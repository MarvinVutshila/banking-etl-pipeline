# Banking ETL Pipeline

This project demonstrates a complete ETL (Extract, Transform, Load) pipeline that processes banking transaction data from a CSV file, cleans and categorizes the data, and loads it into a MySQL database. It also prepares the data for visualization in tools like Metabase.

## Features

- Extracts data from banking CSV files  
- Cleans and filters transaction descriptions  
- Categorizes transactions based on keywords  
- Handles missing numeric data gracefully  
- Loads cleaned data into a MySQL database  
- Securely manages database credentials using environment variables (`.env`)

## Technologies Used

- Python (Pandas, SQLAlchemy, PyMySQL, python-dotenv)  
- MySQL database  
- Metabase (for data visualization)
ss
## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/MarvinVutshila/banking-etl-pipeline.git
   cd banking-etl-pipeline
