import requests
from requests_aws4auth import AWS4Auth
import boto3

region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

ES_ENDPOINT = 'ENTER YOUR END POINT'

url = f"{ES_ENDPOINT}/restaurants"
headers = {"Content-Type": "application/json"}
payload = {
    "mappings": {
        "properties": {
            "RestaurantID": {"type": "keyword"},
            "Cuisine": {"type": "text"}
        }
    }
}

response = requests.put(url, auth=awsauth, headers=headers, json=payload)
print("Response:", response.status_code, response.text)