import pickle

print("⏳ Loading the AI Brain...")

# Load the trained model we just made
with open('vuln_model.pkl', 'rb') as f:
    vectorizer, model = pickle.load(f)

def check_input(text):
    # 1. Convert text to numbers
    vec = vectorizer.transform([text])
    
    # 2. Ask the AI for a prediction
    prediction = model.predict(vec)[0]
    
    # 3. Return the result
    if prediction == 1:
        return "🔴 DANGER: Malicious Input Detected!"
    else:
        return "🟢 SAFE: Looks normal."

# --- TEST ZONE ---
print("\n🤖 AI SECURITY GUARD IS ONLINE")
print("-" * 30)

test_inputs = [
    "Hello friend",
    "admin' OR 1=1 --",
    "search for shoes",
    "<script>alert('hack')</script>",
    "drop table users"
]

for text in test_inputs:
    result = check_input(text)
    print(f"Input: '{text}' \nResult: {result}\n")
