# Superstore Dataset Exploration and Cleaning
# Set CRAN mirror to avoid selection prompt
options(repos = c(CRAN = "https://cloud.r-project.org"))

# Install required packages if not already installed
required_packages <- c("readr", "dplyr", "tidyr", "ggplot2", "lubridate", "skimr", "janitor", "DataExplorer")
new_packages <- required_packages[!required_packages %in% installed.packages()[,"Package"]]
if(length(new_packages) > 0) {
  install.packages(new_packages)
}

# Load libraries
library(readr)
library(dplyr)
library(tidyr)
library(ggplot2)
library(lubridate)
library(skimr)
library(janitor)
library(DataExplorer)

# Read the dataset
superstore <- read_csv("Superstore Dataset.csv")

# Display basic information about the dataset
cat("\n===== DATASET DIMENSIONS =====\n")
cat("Number of rows:", nrow(superstore), "\n")
cat("Number of columns:", ncol(superstore), "\n")

cat("\n===== COLUMN NAMES =====\n")
print(colnames(superstore))

# Check data types
cat("\n===== DATA TYPES =====\n")
str(superstore)

# Check for missing values
cat("\n===== MISSING VALUES =====\n")
missing_values <- colSums(is.na(superstore))
print(missing_values[missing_values > 0])
cat("Total missing values:", sum(is.na(superstore)), "\n")

# Generate comprehensive summary statistics
cat("\n===== SUMMARY STATISTICS =====\n")
skim_result <- skim(superstore)
print(skim_result)

# Clean the dataset
superstore_clean <- superstore %>%
  # Convert date columns to proper date format
  mutate(
    `Order Date` = mdy(`Order Date`),
    `Ship Date` = mdy(`Ship Date`)
  ) %>%
  # Clean column names
  clean_names() %>%
  # Add useful derived columns
  mutate(
    order_year = year(order_date),
    order_month = month(order_date),
    order_day = day(order_date),
    shipping_days = as.numeric(ship_date - order_date),
    profit_margin = profit / sales
  )

# Check for duplicate rows
cat("\n===== DUPLICATE ROWS =====\n")
duplicate_count <- sum(duplicated(superstore))
cat("Number of duplicate rows:", duplicate_count, "\n")

# Check for outliers in key numeric columns
cat("\n===== OUTLIERS CHECK =====\n")
numeric_cols <- c("sales", "quantity", "discount", "profit", "profit_margin", "shipping_days")
for(col in numeric_cols) {
  if(col %in% colnames(superstore_clean)) {
    cat("\nOutliers in", col, ":\n")
    q1 <- quantile(superstore_clean[[col]], 0.25, na.rm = TRUE)
    q3 <- quantile(superstore_clean[[col]], 0.75, na.rm = TRUE)
    iqr <- q3 - q1
    lower_bound <- q1 - 1.5 * iqr
    upper_bound <- q3 + 1.5 * iqr
    outliers <- superstore_clean[[col]][superstore_clean[[col]] < lower_bound | superstore_clean[[col]] > upper_bound]
    cat("Number of outliers:", length(outliers), "\n")
    cat("Min:", min(outliers, na.rm = TRUE), "Max:", max(outliers, na.rm = TRUE), "\n")
  }
}

# Basic distribution of categorical variables
cat("\n===== CATEGORICAL VARIABLES DISTRIBUTION =====\n")
cat("\nCategory distribution:\n")
print(table(superstore_clean$category))

cat("\nSub-Category distribution:\n")
print(table(superstore_clean$sub_category))

cat("\nSegment distribution:\n")
print(table(superstore_clean$segment))

cat("\nRegion distribution:\n")
print(table(superstore_clean$region))

cat("\nShip Mode distribution:\n")
print(table(superstore_clean$ship_mode))

# Save the cleaned dataset
write_csv(superstore_clean, "superstore_clean.csv")
cat("\n===== CLEANED DATASET SAVED =====\n")
cat("Cleaned dataset saved as 'superstore_clean.csv'\n")

# Create a data quality report
cat("\n===== GENERATING DATA QUALITY REPORT =====\n")
DataExplorer::create_report(superstore_clean, output_file = "superstore_data_report.html")
cat("Data quality report generated as 'superstore_data_report.html'\n")

cat("\n===== EXPLORATION COMPLETE =====\n")
