#!/usr/bin/env python3
# Sales Performance by Product Hierarchy Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better visualizations
plt.style.use('ggplot')
sns.set(font_scale=1.1)
plt.rcParams['figure.figsize'] = [10, 6]

# Load the cleaned dataset
print("Loading the cleaned dataset...")
df = pd.read_csv('superstore_clean.csv')

# Display basic information
print(f"Dataset Shape: {df.shape}")
print("\nFirst few rows:")
print(df.head())

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
