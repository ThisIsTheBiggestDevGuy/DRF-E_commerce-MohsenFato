from django.test import TestCase

# all the Unit tests here
# written using, and meant to be used in Postman
# Run EACH unit test Separately

# Listing categories, each one containing its related attributes
import requests

url = "http://localhost:8000/api1/categories/"

payload = ""
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
# End of listing categories Test


# Creating a post
import requests
import json

url = "http://localhost:8000/api1/posts/"
# all the data below, is sample, could be replaced
payload = json.dumps({
  "user": 4,
  "title": "1st Test Post",
  "description": "This is a test post one.",
  "price": 19.99,
  "category": 1,
  "hide_phone_number": False,
  "phone_number": "123-456-7890"
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Token f3e90bea66ec0c8ba05d9ec5d6c956695326c3e2'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
# End of post creation test

# Listing posts Test
import requests

url = "http://localhost:8000/api1/posts/"

payload = ""
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

# End of listing posts Test

# Retrieving a post Test
import requests

url = "http://localhost:8000/api1/posts/1/"

payload = ""
headers = {
  'Authorization': 'Token f3e90bea66ec0c8ba05d9ec5d6c956695326c3e2'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

# End of retrieving post Test

# updating post Test
import requests
import json

url = "http://localhost:8000/api1/posts/1/"

payload = json.dumps({
  "user": 9,
  "title": "1st Test Post updated",
  "description": "This is a test post one, updated.",
  "price": 19.2,
  "category": 3,
  "hide_phone_number": True,
  "phone_number": "123-456-7890"
})
headers = {
  'Authorization': 'Token f3e90bea66ec0c8ba05d9ec5d6c956695326c3e2',
  'Content-Type': 'application/json'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)

# End of updating post test

# Deleting a post Test
import requests

url = "http://localhost:8000/api1/posts/2/"

payload = ""
headers = {
  'Authorization': 'Token f3e90bea66ec0c8ba05d9ec5d6c956695326c3e2'
}

response = requests.request("DELETE", url, headers=headers, data=payload)

print(response.text)

# End of deleting post test
