# src/visualizations.py

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect('data/african_ecommerce.db')

# Read the data into a pandas DataFrame
df = pd.read_sql_query("SELECT * FROM transactions", conn)

# Close the connection
conn.close()

# Convert transaction_date to datetime
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

# 1. Overview
def plot_overview():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 15))
    
    # Total transactions
    ax1.bar(['Total Transactions'], [len(df)])
    ax1.set_title('Total Transactions')
    
    # Total transaction value
    total_value = df['transaction_amount'].sum()
    ax2.bar(['Total Value'], [total_value])
    ax2.set_title(f'Total Transaction Value: ${total_value:,.2f}')
    
    # Fraud rate
    fraud_rate = df['fraud_flag'].mean() * 100
    ax3.pie([fraud_rate, 100-fraud_rate], labels=['Fraud', 'Non-Fraud'], autopct='%1.1f%%')
    ax3.set_title(f'Fraud Rate: {fraud_rate:.2f}%')
    
    # Verification success rate
    success_rate = df['verification_success'].mean() * 100
    ax4.pie([success_rate, 100-success_rate], labels=['Success', 'Failure'], autopct='%1.1f%%')
    ax4.set_title(f'Verification Success Rate: {success_rate:.2f}%')
    
    plt.tight_layout()
    plt.savefig('outputs/figures/overview.png')
    plt.close()

# 2. Fraud Analysis
def plot_fraud_analysis():
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 20))
    
    # Fraud rate by country
    fraud_by_country = df.groupby('country')['fraud_flag'].mean().sort_values(ascending=False)
    fraud_by_country.plot(kind='bar', ax=ax1)
    ax1.set_title('Fraud Rate by Country')
    ax1.set_ylabel('Fraud Rate')
    
    # Fraud rate trend over time
    df_daily = df.groupby(df['transaction_date'].dt.date)['fraud_flag'].mean()
    df_daily.plot(ax=ax2)
    ax2.set_title('Fraud Rate Trend Over Time')
    ax2.set_ylabel('Fraud Rate')
    
    # Fraud rate by verification method
    fraud_by_method = df.groupby('verification_method')['fraud_flag'].mean().sort_values(ascending=False)
    fraud_by_method.plot(kind='bar', ax=ax3)
    ax3.set_title('Fraud Rate by Verification Method')
    ax3.set_ylabel('Fraud Rate')
    
    plt.tight_layout()
    plt.savefig('outputs/figures/fraud_analysis.png')
    plt.close()

# 3. Verification Analysis
def plot_verification_analysis():
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 20))
    
    # Verification success rate by country
    success_by_country = df.groupby('country')['verification_success'].mean().sort_values(ascending=False)
    success_by_country.plot(kind='bar', ax=ax1)
    ax1.set_title('Verification Success Rate by Country')
    ax1.set_ylabel('Success Rate')
    
    # Verification success rate by method
    success_by_method = df.groupby('verification_method')['verification_success'].mean()
    success_by_method.plot(kind='pie', ax=ax2, autopct='%1.1f%%')
    ax2.set_title('Verification Success Rate by Method')
    
    # Verification success rate trend over time
    df_daily = df.groupby(df['transaction_date'].dt.date)['verification_success'].mean()
    df_daily.plot(ax=ax3)
    ax3.set_title('Verification Success Rate Trend Over Time')
    ax3.set_ylabel('Success Rate')
    
    plt.tight_layout()
    plt.savefig('outputs/figures/verification_analysis.png')
    plt.close()

# 4. Transaction Insights
def plot_transaction_insights():
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 20))
    
    # Average transaction amount by device type
    avg_amount = df.groupby('device_type')['transaction_amount'].mean().sort_values(ascending=False)
    avg_amount.plot(kind='bar', ax=ax1)
    ax1.set_title('Average Transaction Amount by Device Type')
    ax1.set_ylabel('Average Amount')
    
    # Transaction volume by hour of day and day of week
    df['hour'] = df['transaction_date'].dt.hour
    df['day'] = df['transaction_date'].dt.dayofweek
    heatmap_data = pd.pivot_table(df, values='transaction_id', index='day', columns='hour', aggfunc='count')
    sns.heatmap(heatmap_data, ax=ax2, cmap='YlOrRd')
    ax2.set_title('Transaction Volume by Hour and Day of Week')
    ax2.set_xlabel('Hour of Day')
    ax2.set_ylabel('Day of Week')
    
    # Top 5 days by transaction volume
    top_days = df.groupby(df['transaction_date'].dt.date)['transaction_id'].count().sort_values(ascending=False).head(5)
    top_days.plot(kind='bar', ax=ax3)
    ax3.set_title('Top 5 Days by Transaction Volume')
    ax3.set_ylabel('Number of Transactions')
    
    plt.tight_layout()
    plt.savefig('outputs/figures/transaction_insights.png')
    plt.close()

# 5. User Demographics
def plot_user_demographics():
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 20))
    
    # Age distribution of users
    df['user_age'].hist(bins=20, ax=ax1)
    ax1.set_title('Age Distribution of Users')
    ax1.set_xlabel('Age')
    ax1.set_ylabel('Count')
    
    # Gender distribution
    df['user_gender'].value_counts().plot(kind='pie', ax=ax2, autopct='%1.1f%%')
    ax2.set_title('Gender Distribution')
    
    # Fraud rate by age group and gender
    df['age_group'] = pd.cut(df['user_age'], bins=[0, 20, 30, 40, 50, 60, 100], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])
    fraud_by_age_gender = df.groupby(['age_group', 'user_gender'])['fraud_flag'].mean().unstack()
    fraud_by_age_gender.plot(kind='bar', ax=ax3)
    ax3.set_title('Fraud Rate by Age Group and Gender')
    ax3.set_xlabel('Age Group')
    ax3.set_ylabel('Fraud Rate')
    
    plt.tight_layout()
    plt.savefig('outputs/figures/user_demographics.png')
    plt.close()

# Run all visualizations
if __name__ == "__main__":
    plot_overview()
    plot_fraud_analysis()
    plot_verification_analysis()
    plot_transaction_insights()
    plot_user_demographics()
    print("All visualizations have been generated and saved in the 'outputs/figures' directory.")