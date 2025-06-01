#!/usr/bin/env python3
# Time-Based Trends and Seasonality Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
from datetime import datetime
import calendar

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
df['order_day_of_week'] = df['order_date'].dt.dayofweek  # Monday=0, Sunday=6
df['order_day_name'] = df['order_date'].dt.day_name()
df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days
df['profit_margin'] = df['profit'] / df['sales']

print("Dataset cleaned and prepared successfully")

# 1. Monthly Sales Trends
print("\n===== MONTHLY SALES TRENDS =====")
# Aggregate sales by month and year
monthly_sales = df.groupby(['order_year', 'order_month']).agg({
    'sales': 'sum',
    'order_id': 'nunique',
    'profit': 'sum'
}).reset_index()

# Create a date column for better plotting
monthly_sales['date'] = pd.to_datetime(monthly_sales['order_year'].astype(str) + '-' + 
                                      monthly_sales['order_month'].astype(str) + '-01')
monthly_sales = monthly_sales.sort_values('date')

# Add month name for better readability
monthly_sales['month_name'] = monthly_sales['date'].dt.strftime('%b')

# Plot monthly sales trends
plt.figure(figsize=(14, 8))
plt.plot(monthly_sales['date'], monthly_sales['sales'], marker='o', linestyle='-', linewidth=2)
plt.title('Monthly Sales Trends (2014-2017)')
plt.xlabel('Month')
plt.ylabel('Sales ($)')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

plt.tight_layout()
plt.savefig('monthly_sales_trends.png')
print("Saved monthly sales trends chart as 'monthly_sales_trends.png'")

# 2. Seasonal Patterns (Sales by Month)
print("\n===== SEASONAL PATTERNS =====")
# Aggregate sales by month (regardless of year)
seasonal_sales = df.groupby('order_month').agg({
    'sales': 'sum',
    'order_id': 'nunique',
    'profit': 'sum'
}).reset_index()

# Add month names
month_names = {i: calendar.month_abbr[i] for i in range(1, 13)}
seasonal_sales['month_name'] = seasonal_sales['order_month'].map(month_names)
seasonal_sales = seasonal_sales.sort_values('order_month')

# Plot seasonal patterns
plt.figure(figsize=(14, 8))

# Plot 1: Sales by Month
plt.subplot(2, 1, 1)
sns.barplot(x='month_name', y='sales', data=seasonal_sales)
plt.title('Sales by Month (Seasonal Pattern)')
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=0)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Plot 2: Order Count by Month
plt.subplot(2, 1, 2)
sns.barplot(x='month_name', y='order_id', data=seasonal_sales)
plt.title('Order Count by Month')
plt.xlabel('Month')
plt.ylabel('Number of Orders')
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig('seasonal_sales_patterns.png')
print("Saved seasonal sales patterns chart as 'seasonal_sales_patterns.png'")

# 3. Year-over-Year Growth Analysis
print("\n===== YEAR-OVER-YEAR GROWTH ANALYSIS =====")
# Aggregate sales by year
yearly_sales = df.groupby('order_year').agg({
    'sales': 'sum',
    'order_id': 'nunique',
    'profit': 'sum'
}).reset_index()

# Calculate year-over-year growth rates
yearly_sales['sales_yoy_growth'] = yearly_sales['sales'].pct_change() * 100
yearly_sales['order_yoy_growth'] = yearly_sales['order_id'].pct_change() * 100
yearly_sales['profit_yoy_growth'] = yearly_sales['profit'].pct_change() * 100

print("Year-over-Year Growth Rates:")
print(yearly_sales)

# Plot year-over-year growth
plt.figure(figsize=(14, 10))

# Plot 1: Total Sales by Year
plt.subplot(2, 2, 1)
sns.barplot(x='order_year', y='sales', data=yearly_sales)
plt.title('Total Sales by Year')
plt.xlabel('Year')
plt.ylabel('Sales ($)')
plt.xticks(rotation=0)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Plot 2: YoY Sales Growth Rate
plt.subplot(2, 2, 2)
sns.barplot(x='order_year', y='sales_yoy_growth', data=yearly_sales[1:])  # Skip first year (no growth rate)
plt.title('Year-over-Year Sales Growth Rate')
plt.xlabel('Year')
plt.ylabel('Growth Rate (%)')
plt.xticks(rotation=0)
plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)  # Add a reference line at 0%

# Plot 3: Total Profit by Year
plt.subplot(2, 2, 3)
sns.barplot(x='order_year', y='profit', data=yearly_sales)
plt.title('Total Profit by Year')
plt.xlabel('Year')
plt.ylabel('Profit ($)')
plt.xticks(rotation=0)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Plot 4: YoY Profit Growth Rate
plt.subplot(2, 2, 4)
sns.barplot(x='order_year', y='profit_yoy_growth', data=yearly_sales[1:])  # Skip first year (no growth rate)
plt.title('Year-over-Year Profit Growth Rate')
plt.xlabel('Year')
plt.ylabel('Growth Rate (%)')
plt.xticks(rotation=0)
plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)  # Add a reference line at 0%

plt.tight_layout()
plt.savefig('yearly_growth_analysis.png')
print("Saved yearly growth analysis chart as 'yearly_growth_analysis.png'")

# 4. Day of Week Analysis
print("\n===== DAY OF WEEK ANALYSIS =====")
# Aggregate sales by day of week
day_of_week_sales = df.groupby('order_day_name').agg({
    'sales': 'sum',
    'order_id': 'nunique',
    'profit': 'sum'
}).reset_index()

# Define day order for proper sorting
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_of_week_sales['day_order'] = day_of_week_sales['order_day_name'].map({day: i for i, day in enumerate(day_order)})
day_of_week_sales = day_of_week_sales.sort_values('day_order')

# Plot day of week patterns
plt.figure(figsize=(14, 8))

# Plot 1: Sales by Day of Week
plt.subplot(2, 1, 1)
sns.barplot(x='order_day_name', y='sales', data=day_of_week_sales, order=day_order)
plt.title('Sales by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=0)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Plot 2: Order Count by Day of Week
plt.subplot(2, 1, 2)
sns.barplot(x='order_day_name', y='order_id', data=day_of_week_sales, order=day_order)
plt.title('Order Count by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Number of Orders')
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig('day_of_week_analysis.png')
print("Saved day of week analysis chart as 'day_of_week_analysis.png'")

# 5. Category Seasonality Analysis
print("\n===== CATEGORY SEASONALITY ANALYSIS =====")
# Aggregate sales by category and month
category_month_sales = df.groupby(['category', 'order_month']).agg({
    'sales': 'sum'
}).reset_index()

# Add month names
category_month_sales['month_name'] = category_month_sales['order_month'].map(month_names)

# Create a pivot table for better visualization
category_month_pivot = category_month_sales.pivot_table(
    index='month_name', 
    columns='category', 
    values='sales'
)

# Reorder months for proper display
category_month_pivot = category_month_pivot.reindex(index=[month_names[i] for i in range(1, 13)])

# Plot category seasonality
plt.figure(figsize=(14, 8))
category_month_pivot.plot(kind='line', marker='o')
plt.title('Sales Seasonality by Product Category')
plt.xlabel('Month')
plt.ylabel('Sales ($)')
plt.grid(True, alpha=0.3)
plt.legend(title='Category')

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

plt.tight_layout()
plt.savefig('category_seasonality.png')
print("Saved category seasonality chart as 'category_seasonality.png'")

# 6. Quarter-over-Quarter Analysis
print("\n===== QUARTER-OVER-QUARTER ANALYSIS =====")
# Aggregate sales by year and quarter
quarterly_sales = df.groupby(['order_year', 'order_quarter']).agg({
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique'
}).reset_index()

# Create a period column for better visualization
quarterly_sales['period'] = quarterly_sales['order_year'].astype(str) + '-Q' + quarterly_sales['order_quarter'].astype(str)
quarterly_sales = quarterly_sales.sort_values(['order_year', 'order_quarter'])

# Plot quarterly trends
plt.figure(figsize=(14, 8))
plt.plot(quarterly_sales['period'], quarterly_sales['sales'], marker='o', linestyle='-', linewidth=2)
plt.title('Quarterly Sales Trends (2014-2017)')
plt.xlabel('Quarter')
plt.ylabel('Sales ($)')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# Format y-axis to show dollar amounts
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

plt.tight_layout()
plt.savefig('quarterly_sales_trends.png')
print("Saved quarterly sales trends chart as 'quarterly_sales_trends.png'")

# 7. Event Merchandise Relevance - Seasonal Recommendations
print("\n===== EVENT MERCHANDISE RELEVANCE =====")
# Identify peak sales months
peak_months = seasonal_sales.sort_values('sales', ascending=False).head(3)
print("Top 3 Sales Months (Best for Events):")
print(peak_months[['month_name', 'sales', 'order_id']])

# Identify top products for peak months
peak_month_ids = peak_months['order_month'].tolist()
peak_month_products = df[df['order_month'].isin(peak_month_ids)].groupby(['category', 'sub-category']).agg({
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique'
}).reset_index().sort_values('sales', ascending=False).head(10)

print("\nTop 10 Products for Peak Sales Months:")
print(peak_month_products)

# Create seasonal merchandise recommendations
seasonal_recommendations = pd.DataFrame({
    'Season': ['Q1 (Winter)', 'Q2 (Spring)', 'Q3 (Summer)', 'Q4 (Holiday)'],
    'Peak Months': ['January, March', 'April, June', 'July, September', 'November, December'],
    'Top Categories': [
        df[df['order_month'].isin([1, 2, 3])].groupby('category')['sales'].sum().idxmax(),
        df[df['order_month'].isin([4, 5, 6])].groupby('category')['sales'].sum().idxmax(),
        df[df['order_month'].isin([7, 8, 9])].groupby('category')['sales'].sum().idxmax(),
        df[df['order_month'].isin([10, 11, 12])].groupby('category')['sales'].sum().idxmax()
    ],
    'Top Sub-Categories': [
        df[df['order_month'].isin([1, 2, 3])].groupby('sub-category')['sales'].sum().nlargest(2).index.tolist(),
        df[df['order_month'].isin([4, 5, 6])].groupby('sub-category')['sales'].sum().nlargest(2).index.tolist(),
        df[df['order_month'].isin([7, 8, 9])].groupby('sub-category')['sales'].sum().nlargest(2).index.tolist(),
        df[df['order_month'].isin([10, 11, 12])].groupby('sub-category')['sales'].sum().nlargest(2).index.tolist()
    ]
})

print("\nSeasonal Merchandise Recommendations:")
print(seasonal_recommendations)

# Save recommendations to CSV
seasonal_recommendations.to_csv('seasonal_merchandise_recommendations.csv', index=False)
print("Saved seasonal merchandise recommendations to 'seasonal_merchandise_recommendations.csv'")

# Save monthly and quarterly data for further reference
monthly_sales.to_csv('monthly_sales_data.csv', index=False)
quarterly_sales.to_csv('quarterly_sales_data.csv', index=False)

print("\n===== ANALYSIS COMPLETE =====")
print("All charts and data files have been saved to the current directory")
