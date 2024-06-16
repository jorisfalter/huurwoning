import requests
from dotenv import load_dotenv
import os
import json
from dateutil import parser
from datetime import datetime, timedelta
from postmarker.core import PostmarkClient
import pytz


### This one serves for a cronjob every 60 minutes

# Load environment variables from .env file
load_dotenv()

# Endpoint URL
url = os.getenv('TOPTAL_GRAPHQL_ENDPOINT')

# Postmark setup
postmark_client = PostmarkClient(server_token=os.getenv('POSTMARK_API_TOKEN'))


# Function to send email
def send_email(subject, body):
    postmark_client.emails.send(
        From='joris@jorisfalter.com',
        To='joris@jorisfalter.com',
        Subject=subject,
        HtmlBody=body
    )

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
      descriptionHast
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
      expectedHours
      estimatedLength{
        verbose
      }
      client {
        city
        fullName
      }
      jobTimeZone{
        timeZone{
          location
          }
      }
    }
    }
}}
'''

## Below two are not available in the initial GQL
# desired start date 
# Application Questions

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

# Get the current time with timezone
current_time = datetime.now(pytz.utc)

# # Get the JSON response body
response_data = response.json()

check_variable = 0

# make job description readable
## make readable
def format_to_html(text):
    # Define headers that should be converted into bullet lists
    bullet_list_headers = [
        "Responsibilities",
        "Required Skills",
        "Nice-to-haves (not mandatory)",
        "Engagement Details"
    ]
    
    # Split the text into lines and process each line
    lines = text.split('\n')
    html_content = ""
    in_bullet_list = False

    for line in lines:
        # Check if the line is a header
        if any(line.startswith(header + ":") for header in bullet_list_headers):
            # Close previous list if any
            if in_bullet_list:
                html_content += "</ul>"
                in_bullet_list = False
            
            html_content += f"<h3>{line}</h3><ul>"
            in_bullet_list = True
        elif in_bullet_list:
            if line.strip() != "":  # Avoid empty lines
                html_content += f"<li>{line}</li>"
        else:
            # Close previous list if not already done
            if in_bullet_list:
                html_content += "</ul>"
                in_bullet_list = False
            
            # Regular header or paragraph
            if line.endswith(':'):
                html_content += f"<h2>{line}</h2>"
            elif line.strip() != "":
                html_content += f"<p>{line}</p>"

    # Close the list if the text ends with bullet points
    if in_bullet_list:
        html_content += "</ul>"

    return html_content

# Iterate over each job entity
for job in response_data['data']['viewer']['eligibleJobs']['entities']:
    # Parse the 'postedWhen' time and convert it to a datetime object
    posted_when = parser.isoparse(job['postedWhen'])
    
    # Calculate the time difference between now and the job's posted time
    time_difference = current_time - posted_when

    # Check if the job was posted in the last 70 minutes - in case the cronjob is delayed
    if time_difference <= timedelta(minutes=70):
        ## Print the job details
        # print(f"Job Title: {job['title']}")
        # print(f"Client City: {job['client']['city']}")
        # print(f"Time Zone: {job['jobTimeZone']['timeZone']['location']}")
        # print(f"Client City: {job['client']['fullName']}")
        # print(f"Length: {job['estimatedLength']['verbose']}")
        # print(f"Expected Hours: {job['expectedHours']}")
        # print(f"Description: {job['description']}\n")
        # print(f"Posted When: {job['postedWhen']}")
        # print(f"Country: {job['client']['countryName']}")
        # print(f"Commitment: {job['commitment']['verbose']}")
        # print("----------------------------------------------------")

        # convert the "description" into headers
        # Convert to HTML
        html_description = format_to_html(job['description'])
        # print(html_content)
        # Iterate through the set and print each element
        # for element in job['description']:
          # print(element)

        # create email
        subject = f"New Job Posted: {job['title']}"
        body = f"""
        <p><strong>Title:</strong> {job['title']}</p>
        <p><strong>Description:</strong> {html_description}</p>
        <p>--------</p>
        <p><strong>Posted When:</strong> {job['postedWhen']}</p>
        <p><strong>Client City:</strong> {job['client']['city']}</p>
        <p><strong>Time Zone:</strong> {job['jobTimeZone']['timeZone']['location']}</p>
        <p><strong>Client Name:</strong> {job['client']['fullName']}</p>
        <p><strong>Length:</strong> {job['estimatedLength']['verbose']}</p>
        <p><strong>Expected Hours:</strong> {job['expectedHours']}</p>
        <p><strong>Country:</strong> {job['client']['countryName']}</p>
        <p><strong>Commitment:</strong> {job['commitment']['verbose']}</p>
        """

        send_email(subject, body)
        print(f"Email sent for job: {job['title']}")

        check_variable = 1

# send email if no email was sent - for testing purposes
        
# # Pretty print everything in the JSON
# pretty_json = json.dumps(response_data, indent=2, ensure_ascii=False)
# # print(pretty_json)

# if check_variable == 0:
#     # create email
#     subject = "No new job"
#     body = pretty_json # sending the response to make sure the connection was made
#     send_email(subject, body)
#     print("email sent without job")

    









