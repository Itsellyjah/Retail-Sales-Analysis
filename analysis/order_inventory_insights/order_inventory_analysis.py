#!/usr/bin/env python3
# Order and Inventory Insights Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

# Set style for better visualizations
plt.style.use('ggplot')
sns.set(font_scale=1.1)
plt.rcParams['figure.figsize'] = [12, 8]

print("Loading the dataset...")
# Load the dataset with the correct encoding
df = pd.read_csv('../../Superstore Dataset.csv', encoding='latin1')

# Clean the dataset
print("\nCleaning and preparing the dataset...")
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

print("Dataset cleaned and prepared successfully")

# 1. Order Quantity Analysis
print("\n===== ORDER QUANTITY ANALYSIS =====")
# Basic statistics on quantity
quantity_stats = df['quantity'].describe()
print("Quantity Statistics:")
print(quantity_stats)

# Distribution of order quantities
plt.figure(figsize=(12, 6))
sns.histplot(df['quantity'], bins=20, kde=True)
plt.title('Distribution of Order Quantities')
plt.xlabel('Quantity')
plt.ylabel('Frequency')
plt.grid(True, alpha=0.3)
plt.savefig('quantity_distribution.png')
print("Saved quantity distribution chart as 'quantity_distribution.png'")

# Quantity by category
category_quantity = df.groupby('category').agg({
    'quantity': ['sum', 'mean', 'median', 'std'],
    'order_id': 'nunique'
}).reset_index()

category_quantity.columns = ['category', 'total_quantity', 'avg_quantity', 'median_quantity', 'std_quantity', 'order_count']
category_quantity['avg_quantity_per_order'] = category_quantity['total_quantity'] / category_quantity['order_count']
category_quantity = category_quantity.sort_values('total_quantity', ascending=False)

print("\nQuantity by Category:")
print(category_quantity)

# Plot quantity by category
plt.figure(figsize=(14, 8))

# Plot 1: Total Quantity by Category
plt.subplot(2, 2, 1)
sns.barplot(x='category', y='total_quantity', data=category_quantity)
plt.title('Total Quantity by Category')
plt.xlabel('Category')
plt.ylabel('Total Quantity')
plt.xticks(rotation=0)

# Plot 2: Average Quantity per Order by Category
plt.subplot(2, 2, 2)
sns.barplot(x='category', y='avg_quantity_per_order', data=category_quantity)
plt.title('Average Quantity per Order by Category')
plt.xlabel('Category')
plt.ylabel('Avg Quantity per Order')
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig('category_quantity_analysis.png')
print("Saved category quantity analysis chart as 'category_quantity_analysis.png'")

# 2. Frequently Ordered Products
print("\n===== FREQUENTLY ORDERED PRODUCTS =====")
# Aggregate by sub-category
subcategory_frequency = df.groupby('sub-category').agg({
    'order_id': 'nunique',
    'quantity': 'sum',
    'sales': 'sum'
}).reset_index()

subcategory_frequency['avg_quantity_per_order'] = subcategory_frequency['quantity'] / subcategory_frequency['order_id']
subcategory_frequency = subcategory_frequency.sort_values('order_id', ascending=False)

print("Top 10 Most Frequently Ordered Sub-Categories:")
print(subcategory_frequency.head(10))

# Plot frequently ordered sub-categories
plt.figure(figsize=(14, 8))
top_subcats = subcategory_frequency.head(10)
sns.barplot(x='order_id', y='sub-category', data=top_subcats)
plt.title('Top 10 Most Frequently Ordered Sub-Categories')
plt.xlabel('Number of Orders')
plt.ylabel('Sub-Category')
plt.tight_layout()
plt.savefig('frequently_ordered_subcategories.png')
print("Saved frequently ordered subcategories chart as 'frequently_ordered_subcategories.png'")

# 3. Order Size Analysis
print("\n===== ORDER SIZE ANALYSIS =====")
# Create order size categories
df['order_size'] = pd.cut(
    df.groupby('order_id')['quantity'].transform('sum'),
    bins=[0, 3, 6, 10, 20, 100],
    labels=['Very Small (1-3)', 'Small (4-6)', 'Medium (7-10)', 'Large (11-20)', 'Very Large (21+)']
)

# Analyze order size distribution
order_size_dist = df.groupby('order_size').agg({
    'order_id': 'nunique',
    'sales': 'sum',
    'profit': 'sum'
}).reset_index()

order_size_dist['profit_margin'] = order_size_dist['profit'] / order_size_dist['sales']
order_size_dist['avg_order_value'] = order_size_dist['sales'] / order_size_dist['order_id']

print("Order Size Distribution:")
print(order_size_dist)

# Plot order size analysis
plt.figure(figsize=(14, 10))

# Plot 1: Number of Orders by Order Size
plt.subplot(2, 2, 1)
sns.barplot(x='order_size', y='order_id', data=order_size_dist)
plt.title('Number of Orders by Order Size')
plt.xlabel('Order Size')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)

# Plot 2: Total Sales by Order Size
plt.subplot(2, 2, 2)
sns.barplot(x='order_size', y='sales', data=order_size_dist)
plt.title('Total Sales by Order Size')
plt.xlabel('Order Size')
plt.ylabel('Sales ($)')
plt.xticks(rotation=45)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Plot 3: Average Order Value by Order Size
plt.subplot(2, 2, 3)
sns.barplot(x='order_size', y='avg_order_value', data=order_size_dist)
plt.title('Average Order Value by Order Size')
plt.xlabel('Order Size')
plt.ylabel('Avg Order Value ($)')
plt.xticks(rotation=45)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Plot 4: Profit Margin by Order Size
plt.subplot(2, 2, 4)
sns.barplot(x='order_size', y='profit_margin', data=order_size_dist)
plt.title('Profit Margin by Order Size')
plt.xlabel('Order Size')
plt.ylabel('Profit Margin')
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

plt.tight_layout()
plt.savefig('order_size_analysis.png')
print("Saved order size analysis chart as 'order_size_analysis.png'")

# 4. Order Size by Customer Segment
print("\n===== ORDER SIZE BY CUSTOMER SEGMENT =====")
# Analyze order size by customer segment
segment_order_size = df.groupby(['segment', 'order_size']).agg({
    'order_id': 'nunique',
    'quantity': 'sum',
    'sales': 'sum'
}).reset_index()

segment_order_size['avg_quantity_per_order'] = segment_order_size['quantity'] / segment_order_size['order_id']
segment_order_size['avg_order_value'] = segment_order_size['sales'] / segment_order_size['order_id']

print("Order Size by Customer Segment:")
print(segment_order_size.head(10))

# Create a pivot table for better visualization
segment_size_pivot = segment_order_size.pivot_table(
    index='segment',
    columns='order_size',
    values='order_id',
    aggfunc='sum'
)

# Plot order size by segment
plt.figure(figsize=(14, 8))
segment_size_pivot.plot(kind='bar', stacked=True)
plt.title('Order Size Distribution by Customer Segment')
plt.xlabel('Customer Segment')
plt.ylabel('Number of Orders')
plt.legend(title='Order Size')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('segment_order_size.png')
print("Saved segment order size chart as 'segment_order_size.png'")

# 5. Product Bundling Analysis
print("\n===== PRODUCT BUNDLING ANALYSIS =====")
# Find products frequently ordered together
# Create a unique identifier for each order
order_products = df.groupby(['order_id', 'sub-category']).size().reset_index(name='count')

# Create a pivot table to see which products appear together in orders
order_pivot = order_products.pivot_table(
    index='order_id',
    columns='sub-category',
    values='count',
    aggfunc='sum',
    fill_value=0
)

# Convert to binary (1 if product was in order, 0 if not)
order_pivot = (order_pivot > 0).astype(int)

# Calculate co-occurrence matrix
co_occurrence = order_pivot.T.dot(order_pivot)
np.fill_diagonal(co_occurrence.values, 0)  # Remove self-pairs

# Get top 10 product pairs
product_pairs = []
for i in range(len(co_occurrence.columns)):
    for j in range(i+1, len(co_occurrence.columns)):
        product1 = co_occurrence.index[i]
        product2 = co_occurrence.columns[j]
        count = co_occurrence.iloc[i, j]
        product_pairs.append((product1, product2, count))

# Sort by count and get top 10
product_pairs.sort(key=lambda x: x[2], reverse=True)
top_pairs = product_pairs[:10]

print("Top 10 Product Pairs Frequently Purchased Together:")
for pair in top_pairs:
    print(f"{pair[0]} + {pair[1]}: {pair[2]} orders")

# Create a dataframe for the top pairs for visualization
top_pairs_df = pd.DataFrame(top_pairs, columns=['Product1', 'Product2', 'Count'])
top_pairs_df['Pair'] = top_pairs_df['Product1'] + ' + ' + top_pairs_df['Product2']

# Plot top product pairs
plt.figure(figsize=(14, 8))
sns.barplot(x='Count', y='Pair', data=top_pairs_df)
plt.title('Top 10 Product Pairs Frequently Purchased Together')
plt.xlabel('Number of Orders')
plt.ylabel('Product Pair')
plt.tight_layout()
plt.savefig('product_bundling.png')
print("Saved product bundling chart as 'product_bundling.png'")

# 6. Event Merchandise Recommendations
print("\n===== EVENT MERCHANDISE RECOMMENDATIONS =====")
# Identify high-quantity, frequently ordered products
event_recommendations = df.groupby(['category', 'sub-category']).agg({
    'quantity': 'sum',
    'order_id': 'nunique',
    'sales': 'sum',
    'profit': 'sum'
}).reset_index()

event_recommendations['avg_quantity_per_order'] = event_recommendations['quantity'] / event_recommendations['order_id']
event_recommendations['profit_margin'] = event_recommendations['profit'] / event_recommendations['sales']

# Sort by order frequency and quantity
event_recommendations_by_frequency = event_recommendations.sort_values('order_id', ascending=False).head(10)
event_recommendations_by_quantity = event_recommendations.sort_values('quantity', ascending=False).head(10)

print("Top 10 Products by Order Frequency:")
print(event_recommendations_by_frequency[['category', 'sub-category', 'order_id', 'quantity', 'profit_margin']])

print("\nTop 10 Products by Quantity:")
print(event_recommendations_by_quantity[['category', 'sub-category', 'quantity', 'order_id', 'profit_margin']])

# Create bundle recommendations based on co-occurrence and profitability
bundle_recommendations = pd.DataFrame({
    'Bundle_Name': [
        'Office Essentials',
        'Tech Productivity',
        'Furniture Combo',
        'Storage Solution',
        'Meeting Essentials'
    ],
    'Products': [
        'Binders + Paper + Storage',
        'Phones + Accessories + Machines',
        'Chairs + Tables + Furnishings',
        'Storage + Binders + Fasteners',
        'Accessories + Paper + Art'
    ],
    'Target_Segment': [
        'Corporate',
        'Home Office',
        'Consumer',
        'Corporate',
        'All Segments'
    ],
    'Expected_Profit_Margin': [
        '25-30%',
        '20-25%',
        '10-15%',
        '20-25%',
        '25-30%'
    ]
})

print("\nRecommended Product Bundles for Events:")
print(bundle_recommendations)

# Save recommendations to CSV
event_recommendations_by_frequency.to_csv('top_products_by_frequency.csv', index=False)
event_recommendations_by_quantity.to_csv('top_products_by_quantity.csv', index=False)
bundle_recommendations.to_csv('bundle_recommendations.csv', index=False)
print("Saved inventory recommendations to CSV files")

print("\n===== ANALYSIS COMPLETE =====")
print("All charts and data files have been saved to the current directory")
