import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def run_ml_analysis():
    # Connect to the SQLite database
    conn = sqlite3.connect('data/african_ecommerce.db')

    # Read into a pd DataFrame
    df = pd.read_sql_query("SELECT * FROM transactions", conn)

    conn.close()


    print("Fraud Distribution:")
    print(df['fraud_flag'].value_counts(normalize=True))

    # Visualize fraud rate by country
    fraud_by_country = df.groupby('country')['fraud_flag'].mean().sort_values(ascending=False)
    fraud_by_country.plot(kind='bar')
    plt.title('Fraud Rate by Country')
    plt.ylabel('Fraud Rate')
    plt.tight_layout()
    plt.savefig('outputs/figures/fraud_rate_by_country.png')
    plt.close()

    # Prepare data for machine learning
    X = pd.get_dummies(df.drop(['transaction_id', 'transaction_date', 'fraud_flag'], axis=1))
    y = df['fraud_flag']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Random Forest model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Make predictions and print classification report
    y_pred = rf_model.predict(X_test)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Feature importance
    feature_importance = pd.DataFrame({'feature': X.columns, 'importance': rf_model.feature_importances_})
    feature_importance = feature_importance.sort_values('importance', ascending=False).head(10)
    feature_importance.plot(x='feature', y='importance', kind='bar')
    plt.title('Top 10 Important Features for Fraud Prediction')
    plt.tight_layout()
    plt.savefig('outputs/figures/feature_importance.png')
    plt.close()

if __name__ == "__main__":
    run_ml_analysis()