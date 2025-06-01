#!/usr/bin/env python3
# Geographic Sales Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
from datetime import datetime

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

# 1. Regional Sales Analysis
print("\n===== REGIONAL SALES ANALYSIS =====")
region_sales = df.groupby('region').agg({
    'sales': 'sum',
    'order_id': 'nunique',
    'profit': 'sum',
    'customer_id': 'nunique'
}).reset_index()

# Calculate metrics
region_sales['avg_sales_per_order'] = region_sales['sales'] / region_sales['order_id']
region_sales['avg_sales_per_customer'] = region_sales['sales'] / region_sales['customer_id']
region_sales['profit_margin'] = region_sales['profit'] / region_sales['sales']
region_sales = region_sales.sort_values('sales', ascending=False)

print(region_sales)

# Visualize regional sales
plt.figure(figsize=(14, 10))

# Plot 1: Total Sales by Region
plt.subplot(2, 2, 1)
sns.barplot(x='region', y='sales', data=region_sales)
plt.title('Total Sales by Region')
plt.ylabel('Sales ($)')
plt.xticks(rotation=0)

# Plot 2: Average Sales per Order by Region
plt.subplot(2, 2, 2)
sns.barplot(x='region', y='avg_sales_per_order', data=region_sales)
plt.title('Average Sales per Order by Region')
plt.ylabel('Avg Sales per Order ($)')
plt.xticks(rotation=0)

# Plot 3: Profit by Region
plt.subplot(2, 2, 3)
sns.barplot(x='region', y='profit', data=region_sales)
plt.title('Total Profit by Region')
plt.ylabel('Profit ($)')
plt.xticks(rotation=0)

# Plot 4: Profit Margin by Region
plt.subplot(2, 2, 4)
sns.barplot(x='region', y='profit_margin', data=region_sales)
plt.title('Profit Margin by Region')
plt.ylabel('Profit Margin')
plt.xticks(rotation=0)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

plt.tight_layout()
plt.savefig('regional_sales_analysis.png')
print("Saved regional sales analysis chart as 'regional_sales_analysis.png'")

# 2. City Sales Analysis
print("\n===== CITY SALES ANALYSIS =====")
# Get top 20 cities by sales
city_sales = df.groupby(['city', 'state', 'region']).agg({
    'sales': 'sum',
    'order_id': 'nunique',
    'profit': 'sum'
}).reset_index()

city_sales['avg_sales_per_order'] = city_sales['sales'] / city_sales['order_id']
city_sales['profit_margin'] = city_sales['profit'] / city_sales['sales']
city_sales = city_sales.sort_values('sales', ascending=False)

print("Top 20 Cities by Sales:")
print(city_sales.head(20))

# Visualize top 10 cities by sales
plt.figure(figsize=(14, 8))
top10_cities = city_sales.head(10)
sns.barplot(x='sales', y='city', data=top10_cities, hue='region', dodge=False)
plt.title('Top 10 Cities by Sales')
plt.xlabel('Sales ($)')
plt.tight_layout()
plt.savefig('top10_cities_sales.png')
print("Saved top 10 cities chart as 'top10_cities_sales.png'")

# 3. Sales Variability Across Regions
print("\n===== SALES VARIABILITY ACROSS REGIONS =====")
# Calculate sales variability metrics
region_variability = df.groupby(['region', 'order_year']).agg({
    'sales': ['sum', 'mean', 'std', 'count']
}).reset_index()

region_variability.columns = ['region', 'year', 'total_sales', 'mean_sales', 'std_sales', 'count']
region_variability['cv'] = region_variability['std_sales'] / region_variability['mean_sales']  # Coefficient of variation

print("Sales Variability by Region and Year:")
print(region_variability)

# Visualize sales variability
plt.figure(figsize=(14, 8))
sns.boxplot(x='region', y='sales', data=df)
plt.title('Sales Distribution by Region')
plt.ylabel('Sales ($)')
plt.tight_layout()
plt.savefig('regional_sales_variability.png')
print("Saved regional sales variability chart as 'regional_sales_variability.png'")

# 4. Seasonal Sales Patterns by Region
print("\n===== SEASONAL SALES PATTERNS BY REGION =====")
seasonal_sales = df.groupby(['region', 'order_year', 'order_quarter']).agg({
    'sales': 'sum'
}).reset_index()

# Create a pivot table for easier visualization
seasonal_pivot = seasonal_sales.pivot_table(
    index=['order_year', 'order_quarter'], 
    columns='region', 
    values='sales'
).reset_index()

print("Seasonal Sales Patterns:")
print(seasonal_pivot.head(10))

# Visualize seasonal patterns
plt.figure(figsize=(16, 8))
for region in df['region'].unique():
    region_data = seasonal_sales[seasonal_sales['region'] == region]
    plt.plot(range(len(region_data)), region_data['sales'], marker='o', label=region)

plt.title('Seasonal Sales Patterns by Region')
plt.xlabel('Time Period (Year-Quarter)')
plt.ylabel('Sales ($)')
plt.legend()
plt.xticks(range(0, len(seasonal_pivot), 2), 
           [f"{year}-Q{quarter}" for year, quarter in 
            zip(seasonal_pivot['order_year'].iloc[::2], seasonal_pivot['order_quarter'].iloc[::2])], 
           rotation=45)
plt.tight_layout()
plt.savefig('seasonal_sales_patterns.png')
print("Saved seasonal sales patterns chart as 'seasonal_sales_patterns.png'")

# 5. Event Merchandise Relevance for Geographic Targeting
print("\n===== EVENT MERCHANDISE RELEVANCE FOR GEOGRAPHIC TARGETING =====")
# Identify high-performing cities for event targeting
event_cities = city_sales[
    (city_sales['sales'] > city_sales['sales'].quantile(0.9)) & 
    (city_sales['profit_margin'] > 0)
].sort_values('sales', ascending=False)

print("Top Cities for Event Targeting (High Sales + Positive Profit Margin):")
print(event_cities[['city', 'state', 'region', 'sales', 'profit_margin']])

# Save results to CSV for further reference
region_sales.to_csv('regional_sales_summary.csv', index=False)
city_sales.head(100).to_csv('top_100_cities.csv', index=False)
event_cities.to_csv('event_target_cities.csv', index=False)
print("\nSaved detailed geographic analysis to CSV files")

print("\n===== ANALYSIS COMPLETE =====")
print("All charts and data files have been saved to the current directory")
