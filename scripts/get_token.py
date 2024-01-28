import requests
import json

# the login endpoint
login_url = "http://localhost:8000/api2/api-token-auth/"

# the login credentials
login_payload = {
    "username": "NewUser3",
    "password": "fuck12345"
}

# sending login request
login_response = requests.post(login_url, data=login_payload)
login_data = login_response.json()

# print the entire response for debugging
print(login_response.text)

# attempt to extract the token
token = login_data.get('token', None)

# print the token if available
if token:
    print(f"Token: {token}")
else:
    print("No token found in the response.")
