import requests

url = "http://localhost:8000/users/auth_user"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsInVzZXJuYW1lIjoiTWF0aWFzIE1henBhcnJvdGUiLCJyb2xlIjoiVXNlciIsImV4cCI6MTc1MTc4MDgzN30.x2ohJhr6zn_F9TRfo_7u8eMBQLNgDRGmU0asp2jucM4"

headers = {
    "Authorization": f"Bearer {token}"
}
response = requests.post(url, headers=headers)

print(f"Status code: {response.status_code}")
print(f"Response: {response.json()}")