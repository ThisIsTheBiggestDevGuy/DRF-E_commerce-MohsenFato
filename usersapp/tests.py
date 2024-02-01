from django.test import TestCase

# all the Unit tests here
# written using, and meant to be used in Postman
# Run EACH unit test Separately

# User registration:
import requests
import json

url = "http://localhost:8000/api2/register/"

payload = json.dumps({
  "username": "testuser",
  "password": "testpassword",
  "email": "test@example.com"
})
headers = {
  'Content-Type': 'application/json',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
# end of registration test

# User login:
import requests
import json

url = "http://localhost:8000/api2/api-token-auth/"

payload = json.dumps({
  "username": "testuser",
  "password": "testpassword"
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Token f3e90bea66ec0c8ba05d9ec5d6c956695326c3e2'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
# End of login test


# Creating seller profile creation
import requests
import json

url = "http://localhost:8000/api2/create-seller-profile/"

payload = json.dumps({
  "contact_info": "tell: +1 1234 123 4567",
  "bio": "this is a company for NewUser3"
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Token f3e90bea66ec0c8ba05d9ec5d6c956695326c3e2'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
# End of seller profile creation test

# Rating and commenting a seller profile
import requests
import json

url = "http://localhost:8000/api2/seller-reviews/"

payload = json.dumps({
  "rating": 4,
  "comment": "kinda good"
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Token f3e90bea66ec0c8ba05d9ec5d6c956695326c3e2'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
# End of commenting test

# Fetching a seller profile with its details
import requests

url = "http://localhost:8000/api2/seller-profile/2/"

payload = ""
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
# end of fetching test
