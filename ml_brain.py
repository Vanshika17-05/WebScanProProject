import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

print("🧠 Waking up the AI...")

# 1. The Training Data
# 0 = Safe (Normal text)
# 1 = Malicious (SQL Injection / XSS attacks)
data = [
    ("select * from users", 1),
    ("admin' or 1=1 --", 1),
    ("<script>alert('hacked')</script>", 1),
    ("drop table users", 1),
    ("union select 1,2,3", 1),
    ("hello world", 0),
    ("my name is vanshika", 0),
    ("search for laptop", 0),
    ("user_id=1234", 0),
    ("login page", 0)
]

# Convert to a nice table (DataFrame)
df = pd.DataFrame(data, columns=['text', 'label'])

# 2. Feature Extraction (Convert words to numbers)
# Machines can't read words, so we turn them into "vectors"
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df['label']

# 3. Train the Model (Naive Bayes)
# This is a standard algorithm for text classification
model = MultinomialNB()
model.fit(X, y)

# 4. Save the Brain
# We save the trained model to a file so we can use it later
with open('vuln_model.pkl', 'wb') as f:
    pickle.dump((vectorizer, model), f)

print("✅ AI Model trained successfully!")
print("💾 Saved as 'vuln_model.pkl'")
