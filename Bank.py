import pandas as pd
import pymysql
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

# Load environment variables from .env file
load_dotenv()

# Get MySQL credentials from .env
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
database = os.getenv("MYSQL_DB")

# URL-encode the password for MySQL URI
password_encoded = quote_plus(password)

# Load your CSV file (update the path if needed)
df = pd.read_csv("testing_fake.csv")

# Step 1: Remove unwanted rows containing "exc w/lim"
df = df[~df['Description'].str.contains('exc w/lim', case=False, na=False)]

# Step 2: Ensure Category and Parent Category columns exist
if 'Category' not in df.columns:
    df['Category'] = ''
if 'Parent Category' not in df.columns:
    df['Parent Category'] = ''

# Step 3: Define categorization logic
def update_category(row):
    description = str(row['Description']).lower()
    if 'decline' in description:
        row['Category'] = 'Card Declined'
        row['Parent Category'] = 'Bank Response'
    elif 'insufficient' in description:
        row['Category'] = 'Failed Transaction'
        row['Parent Category'] = 'System Notice'
    return row


# Step 4: Apply categorization
df = df.apply(update_category, axis=1)


# Step 5: Fill missing values in numeric columns with 0
numeric_cols = ['Money In', 'Money Out', 'Fee', 'Balance']
df[numeric_cols] = df[numeric_cols].fillna(0)


# Step 6: Save cleaned file
df.to_csv("updated_file.csv", index=False)
print("Cleaned file saved as 'updated_file.csv'.")


# Step 7: Connect to MySQL and create database if not exists
conn = pymysql.connect(host=host, user=user, password=password)
cursor = conn.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
print(f"Database '{database}' ready.")
cursor.close()
conn.close()


# Step 8: Connect with SQLAlchemy and upload table
engine = create_engine(f"mysql+pymysql://{user}:{password_encoded}@{host}:3306/{database}")
df.to_sql(name='bank_statements', con=engine, if_exists='replace', index=False)
print("Data uploaded to MySQL table 'bank_statements'.")
