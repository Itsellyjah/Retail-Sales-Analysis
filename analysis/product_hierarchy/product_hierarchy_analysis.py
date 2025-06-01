#!/usr/bin/env python3
# Sales Performance by Product Hierarchy Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style for better visualizations
plt.style.use('ggplot')
sns.set(font_scale=1.1)
plt.rcParams['figure.figsize'] = [12, 8]

# Load the original dataset
print("Loading the dataset...")
df = pd.read_csv('Superstore Dataset.csv', encoding='latin1')

# Display basic information
print(f"Dataset Shape: {df.shape}")
print("\nFirst few rows:")
print(df.head())

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
df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days
df['profit_margin'] = df['profit'] / df['sales']

print("Dataset cleaned successfully")

# 1. Sales by Category
print("\n===== SALES BY CATEGORY =====")
category_sales = df.groupby('category').agg({
    'sales': 'sum',
    'order_id': 'nunique',
    'quantity': 'sum',
    'profit': 'sum'
}).reset_index()

# Calculate metrics
category_sales['avg_sales_per_order'] = category_sales['sales'] / category_sales['order_id']
category_sales['profit_margin'] = category_sales['profit'] / category_sales['sales']
category_sales = category_sales.sort_values('sales', ascending=False)

print(category_sales)

# Visualize sales by category
plt.figure(figsize=(12, 6))
sns.barplot(x='category', y='sales', data=category_sales)
plt.title('Total Sales by Category')
plt.ylabel('Sales ($)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('category_sales.png')
print("Saved category sales chart as 'category_sales.png'")

# 2. Sales by Sub-Category
print("\n===== SALES BY SUB-CATEGORY =====")
subcategory_sales = df.groupby(['category', 'sub-category']).agg({
    'sales': 'sum',
    'order_id': 'nunique',
    'quantity': 'sum',
    'profit': 'sum'
}).reset_index()

# Calculate metrics
subcategory_sales['avg_sales_per_order'] = subcategory_sales['sales'] / subcategory_sales['order_id']
subcategory_sales['profit_margin'] = subcategory_sales['profit'] / subcategory_sales['sales']
subcategory_sales = subcategory_sales.sort_values('sales', ascending=False)

print("Top 10 Sub-Categories by Sales:")
print(subcategory_sales.head(10))

# Visualize top 10 sub-categories by sales
plt.figure(figsize=(14, 8))
top10_subcategories = subcategory_sales.head(10)
sns.barplot(x='sales', y='sub-category', data=top10_subcategories, hue='category', dodge=False)
plt.title('Top 10 Sub-Categories by Sales')
plt.xlabel('Sales ($)')
plt.tight_layout()
plt.savefig('top10_subcategory_sales.png')
print("Saved top 10 sub-categories chart as 'top10_subcategory_sales.png'")

# 3. Top Selling Products
print("\n===== TOP SELLING PRODUCTS =====")
product_sales = df.groupby(['product_name', 'category', 'sub-category']).agg({
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
print(product_sales.head(20)[['product_name', 'category', 'sub-category', 'sales', 'quantity', 'profit', 'profit_margin']])

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
print(event_merchandise.head(10)[['product_name', 'category', 'sub-category', 'sales', 'quantity', 'profit_margin']])

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
