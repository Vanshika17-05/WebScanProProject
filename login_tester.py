
import requests

def test_login(url, username):
    # 1. The list of passwords to attempt
    # (In a real scenario, this would be a file with thousands of passwords)
    common_passwords = [
        "admin", "123456", "password", "admin123", "12345", 
        "pass", "qwerty", "letmein", "welcome", "root"
    ]
    
    results = []
    
    # 2. Fix URL format if needed
    if not url.startswith("http"):
        url = "http://" + url

    # 3. Loop through passwords
    for password in common_passwords:
        try:
            # Send the login request
            # We assume fields are named 'username' and 'password' (common standard)
            payload = {'username': username, 'password': password, 'Login': 'Login'}
            
            # fast timeout so the tool doesn't freeze
            response = requests.post(url, data=payload, timeout=2)
            
            # 4. Analyze the response
            # If the page size changes or keywords like 'incorrect' disappear, it might be a hit
            if "incorrect" not in response.text.lower() and "failed" not in response.text.lower():
                results.append(f"⚠️ POTENTIAL MATCH: {password}")
            else:
                pass # Login failed, which is good for security
                
        except Exception as e:
            return [f"Error connecting: {str(e)}"]

    if not results:
        return ["✅ No weak passwords found from the list."]
    
    return results
