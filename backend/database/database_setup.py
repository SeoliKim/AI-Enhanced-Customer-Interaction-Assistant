import pandas as pd
from sqlalchemy import create_engine
import os

# Create a SQLite database
db_path = 'ecommerce_data.db'
engine = create_engine(f'sqlite:///{db_path}')

# List of CSV files and their corresponding table names
csv_files = {
    'customerDB': 'data/olist_customers_dataset.csv',
    'geolocationDB': 'data/olist_geolocation_dataset.csv',
    'orderItemsDB': 'data/olist_order_items_dataset.csv',
    'orderPaymentDB': 'data/olist_order_payments_dataset.csv',
    'orderReviewDB': 'data/olist_order_reviews_dataset.csv',
    'orderDB': 'data/olist_orders_dataset.csv',
    'productDB': 'data/olist_products_dataset.csv',
    'sellerDB': 'data/olist_sellers_dataset.csv',
    'productCategoryDB': 'data/product_category_name_translation.csv'
}

# Read each CSV file and write it to the SQLite database
for table_name, file_path in csv_files.items():
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Imported {file_path} to table {table_name}")
    else:
        print(f"File not found: {file_path}")

print("Database creation completed.")