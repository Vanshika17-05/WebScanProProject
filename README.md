# WebScanPro 🛡

*WebScanPro* is a lightweight, Python-based automated vulnerability scanner designed to detect common web security flaws such as *SQL Injection (SQLi), **Cross-Site Scripting (XSS), and **IDOR*. It features a modular architecture and generates professional HTML security reports.

---

## 🚀 Key Features

* *Automated Scanning:* Crawls and tests target URLs for vulnerabilities automatically.
* *SQL Injection Detection:* Identifies potential SQLi flaws in URL parameters.
* *XSS Detection:* Checks for Reflected Cross-Site Scripting vulnerabilities.
* *Modular Design:* Built with separate modules for crawling, scanning, and reporting.
* *Professional Reporting:* Generates a color-coded *HTML Report* with findings classified by severity (High, Medium, Low).
* *CLI Interface:* Easy-to-use Command Line Interface (CLI) for quick scanning.

---

## 🛠 Tech Stack

* *Language:* Python 3.x
* *Libraries:* requests, BeautifulSoup4, argparse
* *Output:* HTML/CSS

---

## ⚙ Installation

1.  *Clone the repository:*
    bash
    git clone [https://github.com/yourusername/WebScanPro.git](https://github.com/yourusername/WebScanPro.git)
    cd WebScanPro
    

2.  *Install dependencies:*
    bash
    pip install -r requirements.txt
    

---

## 💻 Usage

Run the tool from the terminal by providing the target URL:

```bash
python main.py -u [http://target-website.com](http://target-website.com)

### completly operational


