
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# --- 1. TOKENIZER ---
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

# --- 2. LOAD & SPLIT DATA ---
print("⏳ Loading dataset...")
df = pd.read_csv("dataset.csv") # Make sure this file exists
df = df.dropna()

# Auto-detect URL column
target_col = df.columns[0]
for col in df.columns:
    if "url" in col.lower():
        target_col = col
        break

X = [str(x) for x in df[target_col].values]
y = df.iloc[:, -1].values

# SPLIT: 80% Train, 20% Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🧠 Training Model... (This might take a minute)")

# --- 3. BUILD PIPELINE ---
model = make_pipeline(
    TfidfVectorizer(tokenizer=make_tokens, token_pattern=None, lowercase=True),
    RandomForestClassifier(n_estimators=100, n_jobs=-1, class_weight="balanced")
)

model.fit(X_train, y_train)

# --- 4. CALCULATE ACCURACY ---
print("📊 Calculating Accuracy...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")
print("\nDetailed Report:\n", classification_report(y_test, y_pred))

# --- 5. SAVE ---
joblib.dump(model, "vuln_model.pkl")
print("💾 Model saved as 'vuln_model.pkl'")