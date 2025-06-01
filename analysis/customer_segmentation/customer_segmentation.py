#!/usr/bin/env python3
# Customer Behavior and Segmentation Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Set style for better visualizations
plt.style.use('ggplot')
sns.set(font_scale=1.1)
plt.rcParams['figure.figsize'] = [12, 8]

# Load the dataset
print("Loading the dataset...")
df = pd.read_csv('Superstore Dataset.csv', encoding='latin1')

# Clean the dataset
print("\nCleaning the dataset...")
# Convert date columns to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

# Clean column names
df.columns = [col.lower().replace(' ', '_') for col in df.columns]

# Add useful derived columns
df['order_year'] = df['order_date'].dt.year
df['order_month'] = df['order_date'].dt.month
df['order_quarter'] = df['order_date'].dt.quarter
df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days
df['profit_margin'] = df['profit'] / df['sales']

print("Dataset cleaned successfully")

# 1. Sales by Customer Segment
print("\n===== SALES BY CUSTOMER SEGMENT =====")
segment_sales = df.groupby('segment').agg({
    'sales': 'sum',
    'order_id': 'nunique',
    'profit': 'sum',
    'customer_id': 'nunique'
}).reset_index()

# Calculate metrics
segment_sales['avg_sales_per_order'] = segment_sales['sales'] / segment_sales['order_id']
segment_sales['avg_sales_per_customer'] = segment_sales['sales'] / segment_sales['customer_id']
segment_sales['profit_margin'] = segment_sales['profit'] / segment_sales['sales']
segment_sales = segment_sales.sort_values('sales', ascending=False)

print(segment_sales)

# Visualize segment sales
plt.figure(figsize=(14, 10))

# Plot 1: Total Sales by Segment
plt.subplot(2, 2, 1)
sns.barplot(x='segment', y='sales', data=segment_sales)
plt.title('Total Sales by Customer Segment')
plt.ylabel('Sales ($)')
plt.xticks(rotation=0)

# Plot 2: Average Sales per Order by Segment
plt.subplot(2, 2, 2)
sns.barplot(x='segment', y='avg_sales_per_order', data=segment_sales)
plt.title('Average Sales per Order by Segment')
plt.ylabel('Avg Sales per Order ($)')
plt.xticks(rotation=0)

# Plot 3: Profit by Segment
plt.subplot(2, 2, 3)
sns.barplot(x='segment', y='profit', data=segment_sales)
plt.title('Total Profit by Segment')
plt.ylabel('Profit ($)')
plt.xticks(rotation=0)

# Plot 4: Profit Margin by Segment
plt.subplot(2, 2, 4)
sns.barplot(x='segment', y='profit_margin', data=segment_sales)
plt.title('Profit Margin by Segment')
plt.ylabel('Profit Margin')
plt.xticks(rotation=0)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

plt.tight_layout()
plt.savefig('segment_sales_analysis.png')
print("Saved segment sales analysis chart as 'segment_sales_analysis.png'")

# 2. Product Category Preferences by Segment
print("\n===== PRODUCT CATEGORY PREFERENCES BY SEGMENT =====")
category_segment = df.groupby(['segment', 'category']).agg({
    'sales': 'sum',
    'order_id': 'nunique'
}).reset_index()

# Calculate percentage of sales within each segment
segment_totals = category_segment.groupby('segment')['sales'].sum().reset_index()
segment_totals.columns = ['segment', 'total_segment_sales']
category_segment = category_segment.merge(segment_totals, on='segment')
category_segment['sales_percentage'] = category_segment['sales'] / category_segment['total_segment_sales']

print(category_segment)

# Visualize category preferences by segment
plt.figure(figsize=(14, 8))
category_pivot = category_segment.pivot_table(
    index='segment', 
    columns='category', 
    values='sales_percentage'
)
category_pivot.plot(kind='bar', stacked=True)
plt.title('Product Category Preferences by Customer Segment')
plt.ylabel('Percentage of Segment Sales')
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.legend(title='Category')
plt.tight_layout()
plt.savefig('category_preferences_by_segment.png')
print("Saved category preferences chart as 'category_preferences_by_segment.png'")

# 3. RFM Analysis (Recency, Frequency, Monetary)
print("\n===== RFM ANALYSIS =====")

# Use the latest date in the dataset as the reference date
reference_date = df['order_date'].max() + timedelta(days=1)
print(f"Reference date for RFM analysis: {reference_date}")

# Calculate RFM metrics for each customer
rfm = df.groupby('customer_id').agg({
    'order_date': lambda x: (reference_date - x.max()).days,  # Recency
    'order_id': 'nunique',  # Frequency
    'sales': 'sum'  # Monetary
}).reset_index()

# Rename columns
rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']

# Add customer name and segment information
customer_info = df[['customer_id', 'customer_name', 'segment']].drop_duplicates()
rfm = rfm.merge(customer_info, on='customer_id')

print("RFM metrics for first 10 customers:")
print(rfm.head(10))

# Create RFM segments
# Convert metrics to scores from 1-5 (5 is best)
rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])  # Reversed for recency (lower is better)
rfm['f_score'] = pd.qcut(rfm['frequency'], 5, labels=[1, 2, 3, 4, 5])
rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

# Calculate RFM Score
rfm['rfm_score'] = rfm['r_score'].astype(int) + rfm['f_score'].astype(int) + rfm['m_score'].astype(int)

# Create RFM Segments
rfm['rfm_segment'] = pd.cut(
    rfm['rfm_score'],
    bins=[0, 5, 9, 12, 15],
    labels=['Low-Value', 'Mid-Value', 'High-Value', 'Top Customers']
)

# Display segment counts
segment_counts = rfm['rfm_segment'].value_counts().reset_index()
segment_counts.columns = ['RFM Segment', 'Count']
print("\nCustomer Counts by RFM Segment:")
print(segment_counts)

# Visualize RFM segments
plt.figure(figsize=(12, 6))
sns.countplot(x='rfm_segment', data=rfm, palette='viridis')
plt.title('Customer Distribution by RFM Segment')
plt.xlabel('RFM Segment')
plt.ylabel('Number of Customers')
plt.tight_layout()
plt.savefig('rfm_segments.png')
print("Saved RFM segments chart as 'rfm_segments.png'")

# 4. Segment Characteristics
print("\n===== SEGMENT CHARACTERISTICS =====")
# Calculate average metrics for each RFM segment
segment_profile = rfm.groupby('rfm_segment').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': 'mean',
    'customer_id': 'count'
}).reset_index()

segment_profile.columns = ['RFM Segment', 'Avg Recency (days)', 'Avg Frequency', 'Avg Monetary', 'Customer Count']
print("RFM Segment Profiles:")
print(segment_profile)

# Visualize segment characteristics
plt.figure(figsize=(16, 12))

# Plot 1: Average Recency by Segment
plt.subplot(2, 2, 1)
sns.barplot(x='RFM Segment', y='Avg Recency (days)', data=segment_profile)
plt.title('Average Recency by Segment')
plt.ylabel('Days Since Last Purchase')
plt.xticks(rotation=45)

# Plot 2: Average Frequency by Segment
plt.subplot(2, 2, 2)
sns.barplot(x='RFM Segment', y='Avg Frequency', data=segment_profile)
plt.title('Average Purchase Frequency by Segment')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)

# Plot 3: Average Monetary Value by Segment
plt.subplot(2, 2, 3)
sns.barplot(x='RFM Segment', y='Avg Monetary', data=segment_profile)
plt.title('Average Monetary Value by Segment')
plt.ylabel('Total Spend ($)')
plt.xticks(rotation=45)

# Plot 4: Customer Count by Segment
plt.subplot(2, 2, 4)
sns.barplot(x='RFM Segment', y='Customer Count', data=segment_profile)
plt.title('Customer Count by Segment')
plt.ylabel('Number of Customers')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('rfm_segment_profiles.png')
print("Saved RFM segment profiles chart as 'rfm_segment_profiles.png'")

# 5. Event Merchandise Relevance
print("\n===== EVENT MERCHANDISE RELEVANCE =====")

# Analyze top customer segments and their product preferences
top_customers = rfm[rfm['rfm_segment'] == 'Top Customers']['customer_id'].tolist()
top_customer_purchases = df[df['customer_id'].isin(top_customers)]

top_category_prefs = top_customer_purchases.groupby(['category', 'sub_category']).agg({
    'sales': 'sum',
    'order_id': 'nunique',
    'profit': 'sum'
}).reset_index().sort_values('sales', ascending=False)

print("Product Preferences of Top Customers:")
print(top_category_prefs.head(10))

# Visualize top customer preferences
plt.figure(figsize=(14, 8))
top_subcats = top_category_prefs.head(10)
sns.barplot(x='sales', y='sub_category', data=top_subcats, hue='category', dodge=False)
plt.title('Top 10 Product Sub-Categories Preferred by Top Customers')
plt.xlabel('Sales ($)')
plt.tight_layout()
plt.savefig('top_customer_preferences.png')
print("Saved top customer preferences chart as 'top_customer_preferences.png'")

# Save results to CSV for further reference
rfm.to_csv('customer_rfm_segments.csv', index=False)
segment_profile.to_csv('rfm_segment_profiles.csv', index=False)
top_category_prefs.head(50).to_csv('top_customer_product_preferences.csv', index=False)
print("\nSaved detailed customer segmentation data to CSV files")

print("\n===== ANALYSIS COMPLETE =====")
print("All charts and data files have been saved to the current directory")
