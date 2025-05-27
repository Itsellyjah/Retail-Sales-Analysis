# Set CRAN mirror
options(repos = c(CRAN = "https://cloud.r-project.org"))

# Install required packages if not already installed
required_packages <- c("rmarkdown", "knitr", "readr", "dplyr", "ggplot2", 
                       "lubridate", "kableExtra", "scales", "DT", "plotly")

for(pkg in required_packages) {
  if(!require(pkg, character.only = TRUE)) {
    install.packages(pkg)
    library(pkg, character.only = TRUE)
  }
}

# Render the R Markdown file
rmarkdown::render("Retail_Sales_Analysis.Rmd", output_format = "html_document")

# Print success message
cat("R Markdown file has been rendered to HTML successfully!\n")
cat("You can now upload the following files to GitHub:\n")
cat("1. train.csv (your data file)\n")
cat("2. Retail_Sales_Analysis.Rmd (R Markdown source)\n")
cat("3. Retail_Sales_Analysis.html (rendered HTML output)\n")
cat("4. README.md (project overview)\n")
cat("5. retail_analysis.R and retail_analysis_advanced.R (R scripts)\n")
