from sqlalchemy import create_engine
import pandas as pd

# Step 1: Connect to the SQL Database
# Replace 'sqlite:///your_database.db' with your database URL
# For example, for MySQL: 'mysql+pymysql://user:password@host/dbname'
engine = create_engine('sqlite:///fishing_reports.db')  # Example for SQLite

# Step 2: Query the Database
# Replace 'your_table' with your actual table name
query = "SELECT * FROM fishing_reports"  # Adjust the SQL query as needed
data = pd.read_sql(query, engine)

# Step 3: Generate the Excel File
output_file = "fishing_reports.xlsx"
data.to_excel(output_file, index=False)

print(f"Excel file created successfully: {output_file}")
