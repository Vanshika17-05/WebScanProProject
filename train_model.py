import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
import joblib

# --- TOKENIZER ---
def make_tokens(f):
    f = str(f)
    tokens_by_slash = f.split('/')
    total_tokens = []
    for i in tokens_by_slash:
        tokens = str(i).split('-')
        tokens_dot = []
        for j in range(0,len(tokens)):
            temp_tokens = str(tokens[j]).split('.')
            tokens_dot = tokens_dot + temp_tokens
        total_tokens = total_tokens + tokens + tokens_dot
    return list(set(total_tokens))

print("⏳ Loading dataset...")

try:
    # Read the full CSV
    df = pd.read_csv("dataset.csv")
    print(f"✅ Raw Data Loaded: {len(df)} rows.")
    print(f"   Columns found: {list(df.columns)}")
except Exception as e:
    print(f"❌ Error reading CSV: {e}")
    exit()

# --- SMART COLUMN DETECTION ---
print("🔍 Analyzing columns to find the URLs...")

url_col = None
label_col = None

for col in df.columns:
    # Check if column name looks like 'url'
    if 'url' in col.lower():
        url_col = col
    # Check if column name looks like 'type' or 'label'
    if 'type' in col.lower() or 'label' in col.lower():
        label_col = col

# Fallback: If we couldn't find names, assume 2nd column is URL (often 1st is ID)
if not url_col:
    # Heuristic: The column with the longest average string length is likely the URL
    # The column with few unique values is likely the label
    print("⚠️ Could not find column named 'url'. Guessing based on data...")
    url_col = df.columns[0] 
    label_col = df.columns[-1]

print(f"   -> Using '{url_col}' as URL data.")
print(f"   -> Using '{label_col}' as Label data.")

# --- PREPARE DATA ---
# Drop rows where URL is missing
df = df.dropna(subset=[url_col, label_col])

# Force conversion to String to prevent 'int' errors
X = df[url_col].astype(str)
y = df[label_col].astype(str)

print(f"🧠 Training on {len(X)} rows... (This will take 1-3 minutes)")

# --- TRAIN ---
model = make_pipeline(
    TfidfVectorizer(tokenizer=make_tokens),
    RandomForestClassifier(n_estimators=100, n_jobs=-1)
)

try:
    model.fit(X, y)
    print("💾 Saving 'vuln_model.pkl'...")
    joblib.dump(model, "vuln_model.pkl")
    print("🚀 SUCCESS! System is upgraded with Real-World Data.")
except Exception as e:
    print(f"❌ Training Failed: {e}")