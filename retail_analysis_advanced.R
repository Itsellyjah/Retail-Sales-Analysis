# Advanced Retail Sales Analysis
# Date: May 27, 2025

# Set CRAN mirror first
options(repos = c(CRAN = "https://cloud.r-project.org"))

# Install and load required packages
required_packages <- c("readr", "dplyr", "ggplot2", "lubridate", "tidyr", "scales", "forcats")
for(pkg in required_packages) {
  if(!require(pkg, character.only = TRUE)) {
    install.packages(pkg)
    library(pkg, character.only = TRUE)
  }
}

# Load the data
retail_data <- read.csv("train.csv", stringsAsFactors = FALSE, check.names = FALSE)

# Clean column names (remove BOM character if present)
names(retail_data)[1] <- "Row ID"

# Data preprocessing
# Convert date columns to Date type
retail_data$`Order Date` <- as.Date(retail_data$`Order Date`, format = "%Y-%m-%d")
retail_data$`Ship Date` <- as.Date(retail_data$`Ship Date`, format = "%Y-%m-%d")

# Calculate shipping days
retail_data$`Shipping Days` <- as.numeric(retail_data$`Ship Date` - retail_data$`Order Date`)

# Extract year and month for time-based analysis
retail_data$Year <- year(retail_data$`Order Date`)
retail_data$Month <- month(retail_data$`Order Date`, label = TRUE)
retail_data$YearMonth <- format(retail_data$`Order Date`, "%Y-%m")

# 1. SALES ANALYSIS

# 1.1 Total sales by category
sales_by_category <- retail_data %>%
  group_by(Category) %>%
  summarise(
    Total_Sales = sum(Sales, na.rm = TRUE),
    Order_Count = n_distinct(`Order ID`),
    Avg_Order_Value = Total_Sales / Order_Count
  ) %>%
  arrange(desc(Total_Sales))

print("Sales by Category:")
print(sales_by_category)

# 1.2 Sales by sub-category
sales_by_subcategory <- retail_data %>%
  group_by(Category, `Sub-Category`) %>%
  summarise(
    Total_Sales = sum(Sales, na.rm = TRUE),
    Order_Count = n_distinct(`Order ID`)
  ) %>%
  arrange(Category, desc(Total_Sales))

print("Sales by Sub-Category:")
print(sales_by_subcategory)

# 1.3 Sales by region
sales_by_region <- retail_data %>%
  group_by(Region) %>%
  summarise(
    Total_Sales = sum(Sales, na.rm = TRUE),
    Order_Count = n_distinct(`Order ID`)
  ) %>%
  arrange(desc(Total_Sales))

print("Sales by Region:")
print(sales_by_region)

# 1.4 Sales by state
sales_by_state <- retail_data %>%
  group_by(State) %>%
  summarise(
    Total_Sales = sum(Sales, na.rm = TRUE),
    Order_Count = n_distinct(`Order ID`)
  ) %>%
  arrange(desc(Total_Sales)) %>%
  head(10)

print("Top 10 States by Sales:")
print(sales_by_state)

# 1.5 Sales by customer segment
sales_by_segment <- retail_data %>%
  group_by(Segment) %>%
  summarise(
    Total_Sales = sum(Sales, na.rm = TRUE),
    Order_Count = n_distinct(`Order ID`),
    Customer_Count = n_distinct(`Customer ID`),
    Avg_Sales_per_Customer = Total_Sales / Customer_Count
  ) %>%
  arrange(desc(Total_Sales))

print("Sales by Customer Segment:")
print(sales_by_segment)

# 2. TIME SERIES ANALYSIS

# 2.1 Monthly sales trend
monthly_sales <- retail_data %>%
  group_by(YearMonth) %>%
  summarise(Total_Sales = sum(Sales, na.rm = TRUE)) %>%
  arrange(YearMonth)

# 2.2 Sales by year and category
yearly_category_sales <- retail_data %>%
  group_by(Year, Category) %>%
  summarise(Total_Sales = sum(Sales, na.rm = TRUE)) %>%
  arrange(Year, desc(Total_Sales))

print("Sales by Year and Category:")
print(yearly_category_sales)

# 3. VISUALIZATIONS

# 3.1 Category sales visualization
p1 <- ggplot(sales_by_category, aes(x = reorder(Category, -Total_Sales), y = Total_Sales)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  geom_text(aes(label = sprintf("$%.1fK", Total_Sales/1000)), vjust = -0.5) +
  labs(title = "Total Sales by Category",
       x = "Category",
       y = "Total Sales ($)") +
  theme_minimal() +
  scale_y_continuous(labels = scales::dollar_format())

print(p1)

# 3.2 Sub-category sales visualization (top 10)
top_subcategories <- retail_data %>%
  group_by(`Sub-Category`) %>%
  summarise(Total_Sales = sum(Sales, na.rm = TRUE)) %>%
  arrange(desc(Total_Sales)) %>%
  head(10)

p2 <- ggplot(top_subcategories, aes(x = reorder(`Sub-Category`, Total_Sales), y = Total_Sales)) +
  geom_bar(stat = "identity", fill = "coral") +
  coord_flip() +
  labs(title = "Top 10 Sub-Categories by Sales",
       x = "Sub-Category",
       y = "Total Sales ($)") +
  theme_minimal() +
  scale_y_continuous(labels = scales::dollar_format())

print(p2)

# 3.3 Regional sales visualization
p3 <- ggplot(sales_by_region, aes(x = reorder(Region, -Total_Sales), y = Total_Sales)) +
  geom_bar(stat = "identity", fill = "darkgreen") +
  geom_text(aes(label = sprintf("$%.1fK", Total_Sales/1000)), vjust = -0.5) +
  labs(title = "Total Sales by Region",
       x = "Region",
       y = "Total Sales ($)") +
  theme_minimal() +
  scale_y_continuous(labels = scales::dollar_format())

print(p3)

# 3.4 Monthly sales trend visualization
monthly_sales$YearMonth <- as.Date(paste0(monthly_sales$YearMonth, "-01"))

p4 <- ggplot(monthly_sales, aes(x = YearMonth, y = Total_Sales)) +
  geom_line(color = "blue") +
  geom_point(color = "red", size = 2) +
  labs(title = "Monthly Sales Trend",
       x = "Month",
       y = "Total Sales ($)") +
  theme_minimal() +
  scale_x_date(date_labels = "%b %Y", date_breaks = "3 months") +
  scale_y_continuous(labels = scales::dollar_format()) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

print(p4)

# 3.5 Segment comparison
p5 <- ggplot(sales_by_segment, aes(x = reorder(Segment, -Total_Sales), y = Total_Sales)) +
  geom_bar(stat = "identity", fill = "purple") +
  geom_text(aes(label = sprintf("$%.1fK", Total_Sales/1000)), vjust = -0.5) +
  labs(title = "Sales by Customer Segment",
       x = "Segment",
       y = "Total Sales ($)") +
  theme_minimal() +
  scale_y_continuous(labels = scales::dollar_format())

print(p5)

# 4. ADDITIONAL ANALYSES

# 4.1 Shipping analysis
shipping_summary <- retail_data %>%
  group_by(`Ship Mode`) %>%
  summarise(
    Avg_Shipping_Days = mean(`Shipping Days`, na.rm = TRUE),
    Order_Count = n_distinct(`Order ID`),
    Total_Sales = sum(Sales, na.rm = TRUE)
  ) %>%
  arrange(`Ship Mode`)

print("Shipping Analysis by Ship Mode:")
print(shipping_summary)

# 4.2 Top customers by sales
top_customers <- retail_data %>%
  group_by(`Customer Name`, `Customer ID`) %>%
  summarise(
    Total_Sales = sum(Sales, na.rm = TRUE),
    Order_Count = n_distinct(`Order ID`)
  ) %>%
  arrange(desc(Total_Sales)) %>%
  head(10)

print("Top 10 Customers by Sales:")
print(top_customers)

# 4.3 Product performance
product_performance <- retail_data %>%
  group_by(`Product Name`, `Product ID`, Category, `Sub-Category`) %>%
  summarise(
    Total_Sales = sum(Sales, na.rm = TRUE),
    Order_Count = n()
  ) %>%
  arrange(desc(Total_Sales)) %>%
  head(10)

print("Top 10 Products by Sales:")
print(product_performance)

# 5. SAVE RESULTS
# Uncomment these lines if you want to save the results

# Save processed data
# write.csv(retail_data, "processed_retail_data.csv", row.names = FALSE)

# Save key analysis results
# write.csv(sales_by_category, "sales_by_category.csv", row.names = FALSE)
# write.csv(sales_by_region, "sales_by_region.csv", row.names = FALSE)
# write.csv(monthly_sales, "monthly_sales.csv", row.names = FALSE)

# Save plots
# ggsave("category_sales.png", plot = p1, width = 10, height = 6)
# ggsave("subcategory_sales.png", plot = p2, width = 10, height = 8)
# ggsave("regional_sales.png", plot = p3, width = 10, height = 6)
# ggsave("monthly_trend.png", plot = p4, width = 12, height = 6)
# ggsave("segment_sales.png", plot = p5, width = 10, height = 6)

# Print session info for reproducibility
sessionInfo()
