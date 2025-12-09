
from xhtml2pdf import pisa
from io import BytesIO
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime

def create_pdf_report(url, prediction, confidence):
    # 1. Prepare Data
    data = {
        "url": url,
        "prediction": prediction.upper(),
        "confidence": f"{confidence:.2f}",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status_class": "danger" if prediction.lower() == "bad" else "safe"
    }

    # 2. Load HTML Template (ABSOLUTE PATH FIX)
    try:
        # Get the folder where THIS python file is located
        current_folder = os.path.dirname(os.path.abspath(__file__))
        
        # Tell Jinja2 to look in that specific folder
        env = Environment(loader=FileSystemLoader(current_folder))
        
        # Now it will definitely find 'template.html'
        template = env.get_template("template.html")
        
        html_content = template.render(data)

        # 3. Convert HTML to PDF
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)

        if pisa_status.err:
            print("❌ PDF Error: Conversion failed.")
            return None
        return pdf_buffer.getvalue()
        
    except Exception as e:
        print(f"❌ PDF Critical Error: {e}")
        return None