#!/usr/bin/env python3
# Sales Performance by Sub-Category Analysis

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

# 1. Sales by Sub-Category
print("\n===== SALES BY SUB-CATEGORY =====")
subcategory_sales = df.groupby(['category', 'sub_category']).agg({
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
sns.barplot(x='sales', y='sub_category', data=top10_subcategories, hue='category', dodge=False)
plt.title('Top 10 Sub-Categories by Sales')
plt.xlabel('Sales ($)')
plt.tight_layout()
plt.savefig('top10_subcategory_sales.png')
print("Saved top 10 sub-categories chart as 'top10_subcategory_sales.png'")

# 2. Sales Distribution within Sub-Categories
print("\n===== SALES DISTRIBUTION WITHIN SUB-CATEGORIES =====")

# Create a boxplot to show sales distribution within each sub-category
plt.figure(figsize=(16, 10))
# Filter to top 10 sub-categories for better visualization
top_subcats = subcategory_sales.head(10)['sub_category'].tolist()
df_top_subcats = df[df['sub_category'].isin(top_subcats)]

# Create boxplot
sns.boxplot(x='sub_category', y='sales', data=df_top_subcats, order=top_subcats)
plt.title('Sales Distribution within Top 10 Sub-Categories')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('subcategory_sales_distribution.png')
print("Saved sub-category sales distribution chart as 'subcategory_sales_distribution.png'")
