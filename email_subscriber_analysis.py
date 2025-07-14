# email_subscriber_analysis.py

import pandas as pd

class EmailAnalyzer:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)

    def generate_report(self, output_file):
        # Simple example: just list domains of subscribers
        domains = self.df['Email'].str.split('@').str[1].value_counts()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Email domain distribution:\n")
            f.write(domains.to_string())