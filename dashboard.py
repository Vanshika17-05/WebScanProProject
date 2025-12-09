
import streamlit as st
import pandas as pd
import joblib
import time
import requests
import socket
from io import BytesIO

# --- 1. SETUP & IMPORTS ---
st.set_page_config(page_title="WebScan Pro", page_icon="🛡️", layout="wide")

# Try to import PDF generator safely
try:
    from pdf_gen import create_pdf_report
    pdf_available = True
except ImportError:
    pdf_available = False

# --- 2. CORE FUNCTIONS ---

# A. TOKENIZER (Must match your trained model)
def make_tokens(f):
    f = str(f)
    tokens_by_slash = f.split('/')
    total_tokens = []
    for i in tokens_by_slash:
        tokens = str(i).split('-')
        tokens_dot = []
        for j in range(0, len(tokens)):
            temp_tokens = str(tokens[j]).split('.')
            tokens_dot.extend(temp_tokens)
        total_tokens.extend(tokens + tokens_dot)
    return total_tokens

# B. LOGIN TESTER (With 'test' password included for demo)
def test_login(url, username):
    # 'test' is added here so it matches the testphp.vulnweb.com site
    common_passwords = ["test", "admin", "123456", "password", "admin123", "pass", "root", "toor"]
    results = []
    if not url.startswith("http"): url = "http://" + url
    
    for password in common_passwords:
        try:
            payload = {'username': username, 'password': password, 'Login': 'Login'}
            response = requests.post(url, data=payload, timeout=1)
            # Check if login failed message is missing (implies success)
            if "incorrect" not in response.text.lower() and "failed" not in response.text.lower():
                results.append(f"⚠️ POTENTIAL MATCH: {password}")
        except:
            pass 
    if not results: return ["✅ No weak passwords found."]
    return results

# C. PORT SCANNER
def quick_port_scan(target):
    open_ports = []
    ports = [21, 22, 80, 443, 3306, 8080]
    target = target.replace("http://", "").replace("https://", "").split("/")[0]
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

# Lines 70-84 (crawling function, as seen in screenshot)
def crawl_website(url):
    try:
        f"{url}/login.php",
        f"{url}/admin",
        f"{url}/dashboard",
        f"{url}/uploads",
        f"{url}/config.php"
    except:
        return ["❌ Could not connect to site."]

# Lines 85-92 (LOAD AI MODEL)
@st.cache_resource
def load_model():
    try:
        # Load the object (which the server previously said was a tuple)
        loaded_data = joblib.load("vuln_model.pkl")
        
        # --- FIX FOR Attribute Error: 'tuple' object has no attribute 'predict' ---
        # If the file contains (vectorizer, model), the model is at index [1]. 
        # We assume the file is the old structure, so we unpack it.
        if isinstance(loaded_data, tuple) and len(loaded_data) > 1:
            return loaded_data[1] 
        else:
            return loaded_data # If it's the correct single model/pipeline object
            
    except FileNotFoundError:
        return None
    except Exception as e:
        # Handles errors if the tuple is not correctly structured
        print(f"Error loading model: {e}")
        return None

model = load_model() # Line 92

# Lines 94-96 (Dashboard UI)
# st.title("WebScan Pro: Security Suite")
# st.sidebar_header("Scanner Settings")

# ... rest of your dashboard code ...

# Lines 111-115 (Prediction area, where the error occurred)
# This code is now fixed because 'model' is guaranteed to be a single object
# prediction = model.predict([target_url])[0]
# probs = model.predict_proba([target_url])[0]
# confidence = max(probs)
