#!/usr/bin/env python3
# Top Selling Products Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better visualizations
plt.style.use('ggplot')
sns.set(font_scale=1.1)
plt.rcParams['figure.figsize'] = [12, 8]

# Load the cleaned dataset
print("Loading the cleaned dataset...")
df = pd.read_csv('superstore_clean.csv')

# Analyze top selling products by name
print("\n===== TOP SELLING PRODUCTS =====")
product_sales = df.groupby(['product_name', 'category', 'sub_category']).agg({
    'sales': 'sum',
    'quantity': 'sum',
    'profit': 'sum',
    'order_id': 'nunique'
}).reset_index()

# Calculate metrics
product_sales['avg_sales_per_order'] = product_sales['sales'] / product_sales['order_id']
product_sales['profit_margin'] = product_sales['profit'] / product_sales['sales']
product_sales = product_sales.sort_values('sales', ascending=False)

print("Top 20 Products by Sales:")
print(product_sales.head(20)[['product_name', 'category', 'sub_category', 'sales', 'quantity', 'profit', 'profit_margin']])

# Visualize top 10 products by sales
plt.figure(figsize=(14, 8))
top10_products = product_sales.head(10)
sns.barplot(x='sales', y='product_name', data=top10_products, hue='category', dodge=False)
plt.title('Top 10 Products by Sales')
plt.xlabel('Sales ($)')
plt.tight_layout()
plt.savefig('top10_products_sales.png')
print("Saved top 10 products chart as 'top10_products_sales.png'")

# Event merchandise relevance analysis
print("\n===== EVENT MERCHANDISE RELEVANCE =====")

# Identify high-demand products with strong profit margins
event_merchandise = product_sales[
    (product_sales['quantity'] > product_sales['quantity'].median()) & 
    (product_sales['profit_margin'] > product_sales['profit_margin'].median())
].sort_values('sales', ascending=False)

print("Top 10 Products for Event Merchandise (High Demand + Good Profit Margin):")
print(event_merchandise.head(10)[['product_name', 'category', 'sub_category', 'sales', 'quantity', 'profit_margin']])

# Create a summary report for event merchandise by category
event_cat_summary = event_merchandise.groupby('category').agg({
    'product_name': 'count',
    'sales': 'sum',
    'profit': 'sum'
}).reset_index()

event_cat_summary.columns = ['Category', 'Product Count', 'Total Sales', 'Total Profit']
print("\nEvent Merchandise Summary by Category:")
print(event_cat_summary)

# Save results to CSV for further reference
product_sales.head(100).to_csv('top_100_products.csv', index=False)
event_merchandise.head(50).to_csv('event_merchandise_recommendations.csv', index=False)
print("\nSaved detailed product analysis to CSV files")

print("\n===== ANALYSIS COMPLETE =====")
print("All charts and data files have been saved to the current directory")
