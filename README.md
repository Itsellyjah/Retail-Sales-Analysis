# Retail Sales Data Analysis

## Overview
This repository contains an analysis of retail sales data using R. The analysis explores sales patterns across different product categories, geographic regions, customer segments, and time periods.

## Files
- `train.csv`: The original retail sales dataset
- `Retail_Sales_Analysis.Rmd`: R Markdown file containing the complete analysis with code and visualizations
- `retail_analysis.R`: Basic R script for initial data exploration
- `retail_analysis_advanced.R`: Advanced R script with detailed analysis
- `Rplots.pdf`: PDF file containing generated plots

## Key Insights
- **Product Categories**: Technology products generate the highest sales ($827,456), followed by Furniture ($728,659) and Office Supplies ($705,422)
- **Geographic Distribution**: The West region leads in sales ($710,220), followed by East ($669,519)
- **Top States**: California is the top-performing state ($446,306), followed by New York ($306,361)
- **Customer Segments**: The Consumer segment accounts for the largest portion of sales ($1,148,061)
- **Time Trends**: Sales show growth over the years 2015-2018
- **Shipping**: Standard Class is the most common shipping mode, while Same Day shipping has the shortest delivery time

## Analysis Components
1. **Sales Analysis**: Breakdown by category, sub-category, and product
2. **Geographic Analysis**: Sales by region and state
3. **Customer Analysis**: Sales by customer segment and top customers
4. **Time Series Analysis**: Monthly trends and yearly comparisons
5. **Product Analysis**: Top-performing products
6. **Shipping Analysis**: Performance by shipping mode

## How to Use
1. Clone this repository
2. Open the R Markdown file (`Retail_Sales_Analysis.Rmd`) in RStudio
3. Install required packages (listed in the setup chunk)
4. Knit the document to generate HTML or PDF output

## Required R Packages
- readr
- dplyr
- ggplot2
- lubridate
- knitr
- kableExtra
- scales
- DT
- plotly

## Future Work
- Predictive modeling to forecast future sales
- Customer segmentation analysis using clustering techniques
- Market basket analysis to identify product associations
- Geographic sales analysis with mapping
- Time series decomposition to identify seasonality and trends
