# Retail Sales Analysis Project

This repository contains a comprehensive analysis of retail sales data from the Superstore dataset. The analysis is organized into several key areas to provide actionable business insights and support event merchandise relevance.

## Project Structure

```
├── analysis/
│   ├── data_cleaning/                # Data preparation and quality assessment
│   ├── product_hierarchy/            # Analysis of sales by product categories
│   ├── geographic_analysis/          # Regional and city-level sales analysis
│   ├── customer_segmentation/        # Customer behavior and RFM analysis
│   ├── time_based_trends/            # Seasonal patterns and growth trends
│   ├── profitability_analysis/       # Profitability and discount impact
│   └── order_inventory_insights/     # Order patterns and bundling opportunities
├── Superstore Dataset.csv            # Original dataset
└── README.md                         # This file
```

## Analysis Areas

### 1. Data Cleaning and Preparation
- Initial data exploration and quality assessment
- Handling data types, missing values, and outliers
- Creating derived metrics (profit margin, shipping days)

### 2. Product Hierarchy Analysis
- Sales performance by Category, Sub-Category, and Product
- Identification of top-selling and most profitable products
- Analysis of product performance for event merchandise relevance

### 3. Geographic Sales Analysis
- Regional and city-level sales patterns
- Sales variability and seasonal trends by region
- Identification of high-potential locations for events

### 4. Customer Segmentation
- RFM (Recency, Frequency, Monetary) analysis
- Customer segment identification and profiling
- Product preferences by customer segment

### 5. Time-Based Trends Analysis
- Monthly sales patterns and seasonal fluctuations
- Year-over-year growth analysis (2015-2017)
- Day-of-week sales distribution
- Category and sub-category seasonality
- Quarterly performance trends

### 6. Profitability and Discount Impact Analysis
- Profit margin by category, sub-category, and region
- Impact of discounts on sales and profitability
- Correlation between discount level and profit
- Identification of negative profit products
- Discount strategy recommendations

### 7. Order and Inventory Insights
- Order quantity distribution and patterns
- Frequently ordered products and categories
- Order size analysis and impact on profitability
- Customer segment ordering patterns
- Product bundling opportunities and recommendations

## Key Insights

### Product Performance
- Technology has the highest profit margin (17.4%) while Furniture has the lowest (2.5%)
- Copiers, Phones, and Accessories are the most profitable sub-categories
- Tables, Bookcases, and Supplies have negative profit margins
- Office Supplies has the highest total quantity ordered (22,906 units)

### Regional Performance
- The West region has the highest profitability (profit per customer: $158)
- The Central region has the lowest profitability ($63 per customer)

### Seasonal Patterns
- Peak sales months are November, December, and September
- Year-over-year growth shows consistent increases from 2015-2017, with 2017 showing 28.3% order growth
- Q4 (Holiday season) shows the strongest sales performance

### Customer Behavior
- Customer segmentation reveals distinct purchasing patterns across segments
- Larger orders (11+ items) have higher profit margins (16.5%)
- Binders, Paper, and Furnishings are the most frequently ordered sub-categories

### Discount Impact
- High discounts (>40%) significantly reduce profit margins and often lead to negative profits
- 26.3% of all orders have negative profit, largely due to excessive discounting
- There's a negative correlation (-0.22) between discount level and profit

### Product Bundling
- Strong co-purchase patterns exist, with Binders+Paper being the most common pair (275 orders)
- Five strategic product bundles were identified for events targeting different customer segments

## Recommendations

### Event Merchandise
- Focus on high-margin, frequently purchased items: Labels, Paper, Envelopes
- Technology products (especially Phones and Accessories) are consistently popular across seasons
- Create targeted bundles like "Office Essentials" (Binders + Paper + Storage) for corporate customers

### Discount Strategy
- Limit discounts to maximum 20% to maintain profitability
- Avoid high discounts (>40%) which consistently lead to negative margins
- Implement tiered discount structure based on order size and customer segment

### Inventory Management
- Prioritize stocking Office Supplies which have highest order frequency and quantity
- Consider seasonal inventory adjustments based on quarterly sales patterns
- Bundle frequently co-purchased items for promotions

## Tools Used
- Python (pandas, matplotlib, seaborn)
- R (tidyverse, lubridate)
- Tableau Public for interactive dashboards
- Git for version control

## Interactive Dashboards

Two interactive Tableau Public dashboards have been created to explore the data:

1. **Regional Sales & Product Performance Dashboard**  
   [View Dashboard on Tableau Public](https://public.tableau.com/app/profile/your.profile/viz/your-dashboard-1)

2. **Customer Segments & Seasonal Trends Dashboard**  
   [View Dashboard on Tableau Public](https://public.tableau.com/app/profile/your.profile/viz/your-dashboard-2)
