
import pandas as pd
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
# --- CORRECTED IMPORT ---
from sklearn.linear_model import LogisticRegression 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# --- 1. TOKENIZER ---
def make_tokens(f):
    f = str(f)
    tokens_by_slash = f.split('/')
    total_tokens = []
    
    for i in tokens_by_slash:
        tokens_dot = []
        temp_tokens = str(i).split('-')
        
        # Inferred loop logic (based on tokenization function context)
        for j in range(0, len(temp_tokens)):
            tokens_dot.extend(str(temp_tokens[j]).split('.'))
        
        total_tokens.extend(temp_tokens)
        total_tokens.extend(tokens_dot)
        
    return total_tokens

# --- 2. TRAINING LOGIC ---
def train_and_save_model():
    # Placeholder: Replace 'dataset.csv' with your actual data file path
    try:
        data = pd.read_csv('dataset.csv') 
    except FileNotFoundError:
        print("Error: dataset.csv not found. Please ensure it's in the project root.")
        return

    # Assuming 'URL' and 'Label' columns based on context
    X = data['URL']
    y = data['Label'] 

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Define the Model Pipeline (using Logistic Regression for smaller file size)
    # This structure is inferred from your imports and logic
    model = Pipeline([
        ('tfidf', TfidfVectorizer(tokenizer=make_tokens, token_pattern=None, lowercase=True)),
        ('clf', LogisticRegression(solver='liblinear', random_state=42)) 
    ])

    print("Training model...")
    model.fit(X_train, y_train) 
    print("Model training complete.")

    # 4. CALCULATE ACCURACY
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    print("\nDetailed Report:\n", classification_report(y_test, y_pred))

    # 5. SAVE
    # This saves the single Pipeline object, ensuring the model.predict() call works.
    joblib.dump(model, "vuln_model.pkl") 
    print("Model saved as 'vuln_model.pkl'")

if __name__ == '__main__':
    train_and_save_model()
