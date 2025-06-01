#!/usr/bin/env python3
# Profitability and Discount Impact Analysis

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
df['profit_margin'] = df['profit'] / df['sales']
df['discount_bin'] = pd.cut(df['discount'], 
                           bins=[-0.001, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0],
                           labels=['0%', '1-10%', '11-20%', '21-30%', '31-40%', '41-50%', '51-100%'])

print("Dataset cleaned and prepared successfully")

# 1. Profitability Analysis by Category and Sub-Category
print("\n===== PROFITABILITY BY CATEGORY AND SUB-CATEGORY =====")
# Aggregate profit metrics by category
category_profit = df.groupby('category').agg({
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique'
}).reset_index()

category_profit['profit_margin'] = category_profit['profit'] / category_profit['sales']
category_profit['avg_profit_per_order'] = category_profit['profit'] / category_profit['order_id']
category_profit = category_profit.sort_values('profit', ascending=False)

print("Profitability by Category:")
print(category_profit)

# Aggregate profit metrics by sub-category
subcategory_profit = df.groupby('sub-category').agg({
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique'
}).reset_index()

subcategory_profit['profit_margin'] = subcategory_profit['profit'] / subcategory_profit['sales']
subcategory_profit['avg_profit_per_order'] = subcategory_profit['profit'] / subcategory_profit['order_id']
subcategory_profit = subcategory_profit.sort_values('profit', ascending=False)

print("\nTop 10 Most Profitable Sub-Categories:")
print(subcategory_profit.head(10))

print("\nLeast Profitable Sub-Categories:")
print(subcategory_profit.tail(5))

# Plot category profitability
plt.figure(figsize=(14, 10))

# Plot 1: Total Profit by Category
plt.subplot(2, 2, 1)
sns.barplot(x='category', y='profit', data=category_profit)
plt.title('Total Profit by Category')
plt.xlabel('Category')
plt.ylabel('Profit ($)')
plt.xticks(rotation=0)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Plot 2: Profit Margin by Category
plt.subplot(2, 2, 2)
sns.barplot(x='category', y='profit_margin', data=category_profit)
plt.title('Profit Margin by Category')
plt.xlabel('Category')
plt.ylabel('Profit Margin')
plt.xticks(rotation=0)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

# Plot 3: Top 5 Sub-Categories by Profit
plt.subplot(2, 2, 3)
top_subcats = subcategory_profit.head(5)
sns.barplot(x='sub-category', y='profit', data=top_subcats)
plt.title('Top 5 Sub-Categories by Profit')
plt.xlabel('Sub-Category')
plt.ylabel('Profit ($)')
plt.xticks(rotation=45)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Plot 4: Bottom 5 Sub-Categories by Profit
plt.subplot(2, 2, 4)
bottom_subcats = subcategory_profit.tail(5)
sns.barplot(x='sub-category', y='profit', data=bottom_subcats)
plt.title('Bottom 5 Sub-Categories by Profit')
plt.xlabel('Sub-Category')
plt.ylabel('Profit ($)')
plt.xticks(rotation=45)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

plt.tight_layout()
plt.savefig('category_profitability.png')
print("Saved category profitability chart as 'category_profitability.png'")

# 2. Regional Profitability Analysis
print("\n===== REGIONAL PROFITABILITY ANALYSIS =====")
# Aggregate profit metrics by region
region_profit = df.groupby('region').agg({
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique',
    'customer_id': pd.Series.nunique
}).reset_index()

region_profit['profit_margin'] = region_profit['profit'] / region_profit['sales']
region_profit['profit_per_order'] = region_profit['profit'] / region_profit['order_id']
region_profit['profit_per_customer'] = region_profit['profit'] / region_profit['customer_id']
region_profit = region_profit.sort_values('profit', ascending=False)

print("Profitability by Region:")
print(region_profit)

# Plot regional profitability
plt.figure(figsize=(14, 10))

# Plot 1: Total Profit by Region
plt.subplot(2, 2, 1)
sns.barplot(x='region', y='profit', data=region_profit)
plt.title('Total Profit by Region')
plt.xlabel('Region')
plt.ylabel('Profit ($)')
plt.xticks(rotation=0)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Plot 2: Profit Margin by Region
plt.subplot(2, 2, 2)
sns.barplot(x='region', y='profit_margin', data=region_profit)
plt.title('Profit Margin by Region')
plt.xlabel('Region')
plt.ylabel('Profit Margin')
plt.xticks(rotation=0)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

# Plot 3: Profit per Order by Region
plt.subplot(2, 2, 3)
sns.barplot(x='region', y='profit_per_order', data=region_profit)
plt.title('Profit per Order by Region')
plt.xlabel('Region')
plt.ylabel('Profit per Order ($)')
plt.xticks(rotation=0)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Plot 4: Profit per Customer by Region
plt.subplot(2, 2, 4)
sns.barplot(x='region', y='profit_per_customer', data=region_profit)
plt.title('Profit per Customer by Region')
plt.xlabel('Region')
plt.ylabel('Profit per Customer ($)')
plt.xticks(rotation=0)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

plt.tight_layout()
plt.savefig('regional_profitability.png')
print("Saved regional profitability chart as 'regional_profitability.png'")

# 3. Discount Impact Analysis
print("\n===== DISCOUNT IMPACT ANALYSIS =====")
# Aggregate metrics by discount bin
discount_impact = df.groupby('discount_bin').agg({
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique',
    'quantity': 'sum'
}).reset_index()

discount_impact['profit_margin'] = discount_impact['profit'] / discount_impact['sales']
discount_impact['avg_order_value'] = discount_impact['sales'] / discount_impact['order_id']
discount_impact['avg_quantity_per_order'] = discount_impact['quantity'] / discount_impact['order_id']

print("Impact of Discounts on Profitability:")
print(discount_impact)

# Plot discount impact
plt.figure(figsize=(16, 12))

# Plot 1: Total Sales by Discount Level
plt.subplot(2, 3, 1)
sns.barplot(x='discount_bin', y='sales', data=discount_impact)
plt.title('Total Sales by Discount Level')
plt.xlabel('Discount Range')
plt.ylabel('Sales ($)')
plt.xticks(rotation=45)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Plot 2: Total Profit by Discount Level
plt.subplot(2, 3, 2)
sns.barplot(x='discount_bin', y='profit', data=discount_impact)
plt.title('Total Profit by Discount Level')
plt.xlabel('Discount Range')
plt.ylabel('Profit ($)')
plt.xticks(rotation=45)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Plot 3: Profit Margin by Discount Level
plt.subplot(2, 3, 3)
sns.barplot(x='discount_bin', y='profit_margin', data=discount_impact)
plt.title('Profit Margin by Discount Level')
plt.xlabel('Discount Range')
plt.ylabel('Profit Margin')
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

# Plot 4: Average Order Value by Discount Level
plt.subplot(2, 3, 4)
sns.barplot(x='discount_bin', y='avg_order_value', data=discount_impact)
plt.title('Average Order Value by Discount Level')
plt.xlabel('Discount Range')
plt.ylabel('Avg Order Value ($)')
plt.xticks(rotation=45)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Plot 5: Average Quantity per Order by Discount Level
plt.subplot(2, 3, 5)
sns.barplot(x='discount_bin', y='avg_quantity_per_order', data=discount_impact)
plt.title('Average Quantity per Order by Discount Level')
plt.xlabel('Discount Range')
plt.ylabel('Avg Quantity per Order')
plt.xticks(rotation=45)

# Plot 6: Order Count by Discount Level
plt.subplot(2, 3, 6)
sns.barplot(x='discount_bin', y='order_id', data=discount_impact)
plt.title('Order Count by Discount Level')
plt.xlabel('Discount Range')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('discount_impact_analysis.png')
print("Saved discount impact analysis chart as 'discount_impact_analysis.png'")

# 4. Discount Impact by Category
print("\n===== DISCOUNT IMPACT BY CATEGORY =====")
# Aggregate metrics by category and discount bin
category_discount = df.groupby(['category', 'discount_bin']).agg({
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique'
}).reset_index()

category_discount['profit_margin'] = category_discount['profit'] / category_discount['sales']

# Create a pivot table for better visualization
category_discount_pivot = category_discount.pivot_table(
    index='discount_bin',
    columns='category',
    values='profit_margin'
)

# Plot discount impact by category
plt.figure(figsize=(14, 8))
sns.heatmap(category_discount_pivot, annot=True, cmap='RdYlGn', fmt='.2%', linewidths=.5)
plt.title('Profit Margin by Category and Discount Level')
plt.xlabel('Category')
plt.ylabel('Discount Range')
plt.tight_layout()
plt.savefig('category_discount_heatmap.png')
print("Saved category discount heatmap as 'category_discount_heatmap.png'")

# 5. Negative Profit Analysis
print("\n===== NEGATIVE PROFIT ANALYSIS =====")
# Identify products with negative profit
negative_profit = df[df['profit'] < 0].groupby(['category', 'sub-category']).agg({
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique',
    'discount': 'mean'
}).reset_index()

negative_profit['profit_margin'] = negative_profit['profit'] / negative_profit['sales']
negative_profit = negative_profit.sort_values('profit')

print("Top 10 Sub-Categories with Negative Profit:")
print(negative_profit.head(10))

# Calculate the percentage of orders with negative profit
total_orders = df['order_id'].nunique()
negative_orders = df[df['profit'] < 0]['order_id'].nunique()
negative_order_percentage = (negative_orders / total_orders) * 100

print(f"\nPercentage of Orders with Negative Profit: {negative_order_percentage:.2f}%")

# Plot negative profit analysis
plt.figure(figsize=(14, 8))
top_negative = negative_profit.head(10)
sns.barplot(x='sub-category', y='profit', data=top_negative)
plt.title('Top 10 Sub-Categories with Negative Profit')
plt.xlabel('Sub-Category')
plt.ylabel('Profit ($)')
plt.xticks(rotation=45)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

plt.tight_layout()
plt.savefig('negative_profit_analysis.png')
print("Saved negative profit analysis chart as 'negative_profit_analysis.png'")

# 6. Correlation between Discount and Quantity
print("\n===== DISCOUNT-QUANTITY CORRELATION =====")
# Calculate correlation
discount_quantity_corr = df[['discount', 'quantity', 'sales', 'profit']].corr()
print("Correlation Matrix:")
print(discount_quantity_corr)

# Plot correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(discount_quantity_corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=.5)
plt.title('Correlation between Discount, Quantity, Sales, and Profit')
plt.tight_layout()
plt.savefig('discount_correlation_heatmap.png')
print("Saved discount correlation heatmap as 'discount_correlation_heatmap.png'")

# 7. Event Merchandise Recommendations
print("\n===== EVENT MERCHANDISE RECOMMENDATIONS =====")
# Identify high-profit, low-discount products for events
event_recommendations = df.groupby(['category', 'sub-category']).agg({
    'sales': 'sum',
    'profit': 'sum',
    'discount': 'mean',
    'quantity': 'sum',
    'order_id': 'nunique'
}).reset_index()

event_recommendations['profit_margin'] = event_recommendations['profit'] / event_recommendations['sales']
event_recommendations['avg_quantity_per_order'] = event_recommendations['quantity'] / event_recommendations['order_id']

# Filter for positive profit and sort by profit margin
event_recommendations = event_recommendations[event_recommendations['profit'] > 0]
event_recommendations = event_recommendations.sort_values('profit_margin', ascending=False)

print("Top 10 High-Margin Products for Event Merchandise:")
print(event_recommendations.head(10))

# Create discount strategy recommendations
discount_strategy = pd.DataFrame({
    'Discount_Range': ['0%', '1-10%', '11-20%', '21-30%', '31-40%', '41-50%', '51-100%'],
    'Recommended_For': [
        'High-margin technology products and premium office supplies',
        'Most products - good balance of sales volume and profitability',
        'Office supplies and selected furniture items',
        'Furniture items to boost sales volume',
        'Limited use - significant profit impact',
        'Avoid - typically results in negative profit',
        'Avoid - consistently negative profit margins'
    ],
    'Expected_Profit_Impact': [
        'Highest profit margins (15-20%)',
        'Good profit margins (10-15%)',
        'Moderate profit margins (5-10%)',
        'Low profit margins (0-5%)',
        'Risk of negative margins',
        'Typically negative margins',
        'Consistently negative margins'
    ]
})

print("\nDiscount Strategy Recommendations:")
print(discount_strategy)

# Save recommendations to CSV
event_recommendations.head(20).to_csv('high_profit_merchandise_recommendations.csv', index=False)
discount_strategy.to_csv('discount_strategy_recommendations.csv', index=False)
print("Saved merchandise and discount recommendations to CSV files")

print("\n===== ANALYSIS COMPLETE =====")
print("All charts and data files have been saved to the current directory")
