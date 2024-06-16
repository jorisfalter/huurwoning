import requests
from dotenv import load_dotenv
import os
import json


# Load environment variables from .env file
load_dotenv()

# Endpoint URL
url = os.getenv('TOPTAL_GRAPHQL_ENDPOINT')

# GraphQL query
query = '''
query GetEligibleJobs {
viewer{
  eligibleJobs {
    totalCount
    page
    entities {
      id
      title
      description
      postedWhen
      workType {
        slug
        verbose
      }
      client {
        countryName
      }
      commitment {
        verbose
      }
    }
    }
}}
'''

# JSON payload
payload = {
    'query': query,
    'operationName': 'GetEligibleJobs'
}

# Headers, including the session cookie if needed
headers = {
    'Content-Type': 'application/json',
    'Cookie': os.getenv('TOPTAL_SESSION_ID')
}


# Make the POST request
response = requests.post(url, json=payload, headers=headers)

# Print the response
# print(response.json())

# Get the JSON response body
response_data = response.json()

# Pretty print JSON
pretty_json = json.dumps(response_data, indent=2, ensure_ascii=False)
print(pretty_json)
