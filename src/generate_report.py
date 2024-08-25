import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from io import BytesIO

def create_plot(df, plot_function, filename):
    plt.figure(figsize=(10, 6))
    plot_function(df)
    plt.tight_layout()
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return img_buffer

def generate_report():
    # Connect to the database and load the data
    conn = sqlite3.connect('data/african_ecommerce.db')
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()

    # Convert transaction_date to datetime
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])

    # Create the PDF document
    doc = SimpleDocTemplate("outputs/reports/african_ecommerce_report.pdf", pagesize=letter,
                            rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

    Story = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

    # Title
    Story.append(Paragraph("African E-commerce Analysis Report", styles['Title']))
    Story.append(Spacer(1, 12))

    # Introduction
    Story.append(Paragraph("This report presents an analysis of e-commerce transactions in Africa, focusing on digital identity verification and fraud patterns.", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Data Overview
    Story.append(Paragraph("1. Data Overview", styles['Heading2']))
    Story.append(Paragraph(f"The dataset contains {len(df)} transactions spanning from {df['transaction_date'].min().date()} to {df['transaction_date'].max().date()}.", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Fraud Analysis
    Story.append(Paragraph("2. Fraud Analysis", styles['Heading2']))
    
    # Fraud rate
    fraud_rate = df['fraud_flag'].mean() * 100
    Story.append(Paragraph(f"The overall fraud rate is {fraud_rate:.2f}%.", styles['Normal']))
    
    # Fraud by country
    img_buffer = create_plot(df, lambda df: sns.barplot(x=df['country'], y=df['fraud_flag']), "fraud_by_country.png")
    Story.append(Image(img_buffer, width=6*inch, height=4*inch))
    Story.append(Paragraph("Fraud Rate by Country", styles['Center']))
    Story.append(Paragraph("The chart above shows the fraud rate by country. " + 
                           f"{df.groupby('country')['fraud_flag'].mean().idxmax()} has the highest fraud rate, " +
                           f"while {df.groupby('country')['fraud_flag'].mean().idxmin()} has the lowest.", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Verification Analysis
    Story.append(Paragraph("3. Verification Analysis", styles['Heading2']))
    
    # Verification success rate
    success_rate = df['verification_success'].mean() * 100
    Story.append(Paragraph(f"The overall verification success rate is {success_rate:.2f}%.", styles['Normal']))
    
    # Verification by method
    img_buffer = create_plot(df, lambda df: sns.barplot(x=df['verification_method'], y=df['verification_success']), "verification_by_method.png")
    Story.append(Image(img_buffer, width=6*inch, height=4*inch))
    Story.append(Paragraph("Verification Success Rate by Method", styles['Center']))
    Story.append(Paragraph("The chart above shows the verification success rate by method. " + 
                           f"{df.groupby('verification_method')['verification_success'].mean().idxmax()} has the highest success rate, " +
                           f"while {df.groupby('verification_method')['verification_success'].mean().idxmin()} has the lowest.", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Transaction Insights
    Story.append(Paragraph("4. Transaction Insights", styles['Heading2']))
    
    # Average transaction amount
    avg_amount = df['transaction_amount'].mean()
    Story.append(Paragraph(f"The average transaction amount is ${avg_amount:.2f}.", styles['Normal']))
    
    # Transaction amount by device type
    img_buffer = create_plot(df, lambda df: sns.boxplot(x=df['device_type'], y=df['transaction_amount']), "amount_by_device.png")
    Story.append(Image(img_buffer, width=6*inch, height=4*inch))
    Story.append(Paragraph("Transaction Amount by Device Type", styles['Center']))
    Story.append(Paragraph("The boxplot above shows the distribution of transaction amounts by device type. " + 
                           f"{df.groupby('device_type')['transaction_amount'].mean().idxmax()} transactions have the highest average amount, " +
                           f"while {df.groupby('device_type')['transaction_amount'].mean().idxmin()} transactions have the lowest.", styles['Normal']))
    Story.append(Spacer(1, 12))

    # User Demographics
    Story.append(Paragraph("5. User Demographics", styles['Heading2']))
    
    # Age distribution
    img_buffer = create_plot(df, lambda df: sns.histplot(df['user_age'], kde=True), "age_distribution.png")
    Story.append(Image(img_buffer, width=6*inch, height=4*inch))
    Story.append(Paragraph("User Age Distribution", styles['Center']))
    Story.append(Paragraph(f"The average user age is {df['user_age'].mean():.1f} years. " +
                           f"The youngest user is {df['user_age'].min()} and the oldest is {df['user_age'].max()}.", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Conclusion
    Story.append(Paragraph("6. Conclusion", styles['Heading2']))
    Story.append(Paragraph("Based on the analysis, we can conclude that:", styles['Normal']))
    Story.append(Paragraph("1. Fraud is a significant issue, with some countries having higher rates than others.", styles['Normal']))
    Story.append(Paragraph("2. Verification methods vary in effectiveness and might need improvement.", styles['Normal']))
    Story.append(Paragraph("3. Transaction patterns differ across device types, which could inform marketing strategies.", styles['Normal']))
    Story.append(Paragraph("4. User demographics show a wide age range, suggesting diverse customer segments.", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Recommendations
    Story.append(Paragraph("7. Recommendations", styles['Heading2']))
    Story.append(Paragraph("1. Focus fraud prevention efforts on high-risk countries.", styles['Normal']))
    Story.append(Paragraph("2. Improve less effective verification methods or phase them out.", styles['Normal']))
    Story.append(Paragraph("3. Tailor marketing and user experience based on device type preferences.", styles['Normal']))
    Story.append(Paragraph("4. Develop targeted strategies for different age groups in the customer base.", styles['Normal']))

    # Build the PDF
    doc.build(Story)
    print("Report generated: outputs/reports/african_ecommerce_report.pdf")

if __name__ == "__main__":
    generate_report()