
# 🛡️ WebScan Pro - AI-Powered Security Suite

**WebScan Pro** is a comprehensive cybersecurity tool designed to detect malicious URLs, potential phishing attacks, and server vulnerabilities using Machine Learning and automated auditing techniques.

## 🚀 Key Features

* **🧠 AI Vulnerability Scanner:** Uses a Random Forest model trained on 40,000+ URLs to predict if a link is safe or malicious (Phishing/Malware).
* **🕷️ Web Crawler:** Automatically maps out a target website, discovering hidden links and pages.
* **🔌 Port Scanner:** Audits the target server for open network ports (FTP, SSH, HTTP, etc.) to identify entry points.
* **🔓 Login Auditor:** Performs dictionary attacks on login pages to test for weak credentials (e.g., "admin123").
* **📄 PDF Reporting:** Generates professional-grade security reports with a single click.

## 📊 Performance
* **Model Accuracy:** [YOUR ACCURACY HERE]% (Calculated on test split)
* **Algorithm:** Random Forest Classifier with Custom Tokenization (TF-IDF).

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Machine Learning:** Scikit-Learn, Pandas, Joblib
* **Web Framework:** Streamlit
* **Tools:** BeautifulSoup4 (Crawling), Socket (Networking), ReportLab/XHTML2PDF (Reporting)

## 📦 Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/your-username/WebScan-Pro.git](https://github.com/your-username/WebScan-Pro.git)
    ```
2.  Install dependencies:
    ```bash
    pip install pandas scikit-learn streamlit requests beautifulsoup4 xhtml2pdf
    ```
3.  Train the Model:
    ```bash
    python train_model.py
    ```
4.  Run the Dashboard:
    ```bash
    streamlit run dashboard.py
    ```

## ⚠️ Disclaimer
This tool is for **Educational Purposes Only**. Do not use this tool on websites you do not own or do not have explicit permission to scan. The developer is not responsible for misuse.