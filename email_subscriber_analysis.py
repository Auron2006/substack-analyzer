# email_subscriber_analysis.py

import pandas as pd
import os

class EmailAnalyzer:
    def __init__(self, csv_file=None):
        if csv_file is None:
            csv_file = None
            for file in os.listdir():
                if file.endswith('.csv'):
                    csv_file = file
                    break
            if not csv_file:
                raise FileNotFoundError("No CSV file found in the current directory.")
        self.df = pd.read_csv(csv_file)

    def generate_report(self, output_file):
        import re
        self.report_lines = []
        if 'Email' not in self.df.columns:
            raise ValueError("CSV must contain a column named 'Email'")

        # Normalize emails and extract domains
        self.df['Email'] = self.df['Email'].astype(str).str.lower()
        self.df['Domain'] = self.df['Email'].str.extract(r'@(.+)$')[0]

        total = len(self.df)
        valid_emails = self.df['Domain'].notna().sum()
        duplicate_count = self.df.duplicated(subset='Email').sum()

        self.report_lines.append(f"Total subscribers: {total}")
        self.report_lines.append(f"Valid email addresses: {valid_emails} ({valid_emails / total:.1%})")
        self.report_lines.append(f"Duplicate emails: {duplicate_count}")

        domain_counts = self.df['Domain'].value_counts()
        self.report_lines.append("\nTop email domains:")
        self.report_lines.append(domain_counts.head(10).to_string())

        free_providers = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com']
        self.df['EmailType'] = self.df['Domain'].apply(lambda d: 'Free' if d in free_providers else 'Corporate')
        type_counts = self.df['EmailType'].value_counts()
        self.report_lines.append("\nFree vs Corporate emails:")
        self.report_lines.append(type_counts.to_string())

        if 'Signup Date' in self.df.columns:
            try:
                self.df['Signup Date'] = pd.to_datetime(self.df['Signup Date'], errors='coerce')
                signup_by_month = self.df.dropna(subset=['Signup Date'])['Signup Date'].dt.to_period('M').value_counts().sort_index()
                self.report_lines.append("\nSign-ups per month:")
                self.report_lines.append(signup_by_month.to_string())
            except Exception as e:
                self.report_lines.append(f"\nSignup Date processing failed: {str(e)}")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.report_lines))