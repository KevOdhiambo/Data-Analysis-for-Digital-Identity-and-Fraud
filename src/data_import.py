import sqlite3
import pandas as pd

def import_data():
    # Create a connection to the SQLite database
    conn = sqlite3.connect('data/african_ecommerce.db')

    # Read the CSV file
    df = pd.read_csv('data/african_ecommerce_transactions.csv')

    # Write dataframe to a SQL table
    df.to_sql('transactions', conn, if_exists='replace', index=False)

    print("Data imported to SQLite database 'data/african_ecommerce.db'")

    # end connection
    conn.close()

if __name__ == "__main__":
    import_data()