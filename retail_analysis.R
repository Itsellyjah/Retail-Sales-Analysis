# Retail Sales Analysis
# Date: May 27, 2025

# Set CRAN mirror first
options(repos = c(CRAN = "https://cloud.r-project.org"))

# Install and load required packages
if (!require("readr")) install.packages("readr")
if (!require("dplyr")) install.packages("dplyr")
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("lubridate")) install.packages("lubridate")

library(readr)
library(dplyr)
library(ggplot2)
library(lubridate)

# Set working directory to the location of the script
# setwd("/path/to/your/directory") # Uncomment and modify if needed

# Load the data
print("Loading the retail sales data...")
retail_data <- read.csv("train.csv", stringsAsFactors = FALSE, check.names = FALSE)

# Display the structure of the data
str(retail_data)

# View the first few rows
head(retail_data)

# Summary statistics
summary(retail_data)

# Check for missing values
colSums(is.na(retail_data))

# Convert date columns to Date type
print("Converting date columns...")
try({
  retail_data$`Order Date` <- mdy(retail_data$`Order Date`)
  retail_data$`Ship Date` <- mdy(retail_data$`Ship Date`)
}, silent = TRUE)

# Basic analysis
print("Performing basic analysis...")

# Total sales by category
sales_by_category <- retail_data %>%
  group_by(Category) %>%
  summarise(Total_Sales = sum(Sales, na.rm = TRUE)) %>%
  arrange(desc(Total_Sales))

print("Sales by Category:")
print(sales_by_category)

# Sales by region
sales_by_region <- retail_data %>%
  group_by(Region) %>%
  summarise(Total_Sales = sum(Sales, na.rm = TRUE)) %>%
  arrange(desc(Total_Sales))

print("Sales by Region:")
print(sales_by_region)

print("Creating visualizations...")

# Visualize sales by category
p1 <- ggplot(sales_by_category, aes(x = reorder(Category, -Total_Sales), y = Total_Sales)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  labs(title = "Total Sales by Category",
       x = "Category",
       y = "Total Sales") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

print(p1)

# Visualize sales by region
p2 <- ggplot(sales_by_region, aes(x = reorder(Region, -Total_Sales), y = Total_Sales)) +
  geom_bar(stat = "identity", fill = "coral") +
  labs(title = "Total Sales by Region",
       x = "Region",
       y = "Total Sales") +
  theme_minimal()

print(p2)

# Time series analysis if date conversion worked
try({
  print("Performing time series analysis...")
  # Monthly sales trend
  monthly_sales <- retail_data %>%
    mutate(Month = floor_date(`Order Date`, "month")) %>%
    group_by(Month) %>%
    summarise(Total_Sales = sum(Sales, na.rm = TRUE))

  p3 <- ggplot(monthly_sales, aes(x = Month, y = Total_Sales)) +
    geom_line() +
    geom_point() +
    labs(title = "Monthly Sales Trend",
         x = "Month",
         y = "Total Sales") +
    theme_minimal()
  
  print(p3)
}, silent = TRUE)

# Save processed data if needed
# write.csv(retail_data, "processed_retail_data.csv", row.names = FALSE)
