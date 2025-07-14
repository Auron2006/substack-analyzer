# streamlit_app.py

import streamlit as st
from email_subscriber_analysis import EmailAnalyzer
import os

st.title("📊 Substack Email Subscriber Analyzer")
st.write("Upload your Substack email export (`full_email.csv`) to analyze your audience.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    csv_filename = "full_email.csv"
    with open(csv_filename, "wb") as f:
        f.write(uploaded_file.read())

    analyzer = EmailAnalyzer(csv_filename)
    with st.spinner("Analyzing data..."):
        analyzer.generate_report("email_analysis_report.txt")

    st.success("Analysis complete!")
    with open("email_analysis_report.txt", "r", encoding="utf-8") as f:
        st.download_button("📄 Download Full Report", f, file_name="email_analysis_report.txt")