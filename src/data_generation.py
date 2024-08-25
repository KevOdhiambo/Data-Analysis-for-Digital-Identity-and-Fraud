import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data():
    # Set random seed for reproducibility
    np.random.seed(42)

    # Generate data
    n_records = 100000
    date_today = datetime.now()
    date_start = date_today - timedelta(days=365)

    data = {
        'transaction_id': range(1, n_records + 1),
        'transaction_date': pd.date_range(start=date_start, end=date_today, periods=n_records),
        'country': np.random.choice(['Nigeria', 'Kenya', 'South Africa', 'Ghana', 'Egypt'], n_records),
        'transaction_amount': np.random.uniform(10, 1000, n_records).round(2),
        'verification_method': np.random.choice(['OTP', 'biometric', 'document_scan'], n_records),
        'verification_success': np.random.choice([True, False], n_records, p=[0.9, 0.1]),
        'fraud_flag': np.random.choice([True, False], n_records, p=[0.05, 0.95]),
        'user_age': np.random.randint(18, 70, n_records),
        'user_gender': np.random.choice(['Male', 'Female'], n_records),
        'device_type': np.random.choice(['Mobile', 'Desktop', 'Tablet'], n_records)
    }

    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv('data/african_ecommerce_transactions.csv', index=False)

    print("Dataset generated and saved to 'data/african_ecommerce_transactions.csv'")

if __name__ == "__main__":
    generate_data()