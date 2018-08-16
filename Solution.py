import json
import requests
import pprint
import time

print('\n')
print("""
Response codes to identify requests:

1	1xx: Informational
It means the request was received and the process is continuing.

2	2xx: Success
It means the action was successfully received, understood, and accepted.

3	3xx: Redirection
It means further action must be taken in order to complete the request.

4	4xx: Client Error
It means the request contains incorrect syntax or cannot be fulfilled.

5	5xx: Server Error
It means the server failed to fulfill an apparently valid request.

""")
print('\n')


## Retrieve request from source url
sourceUrl = "https://api.github.com/orgs/boomtownroi"
sourceResponse = requests.get(url=sourceUrl)
json_data = json.loads(sourceResponse.text)


## Retrieve response from source url
try:
    print("Retrieving request from Top Level: ")
    sourceResponse = requests.get(url=sourceUrl)
    print(sourceResponse)
    print("Error Check Returned:")
    print(sourceResponse.raise_for_status())
    print(sourceResponse.status_code)
    pprint.pprint(json_data)
    print('\n')
except requests.exceptions.HTTPError as err:
    print(err)



# Find urls within JSON object
listOfUrls = []

for name, containedUrl in json_data.items():
    if '_url' in name:
        if 'https://api.github.com/orgs/BoomTownROI' in containedUrl:
            listOfUrls.append(containedUrl)

print("List of found URLs")
print(listOfUrls)
print('\n')
print('\n')

# Locate and access URL json objects in Boomtown Repos
for item in listOfUrls:
    print('URL: ' + item + '\n')
    try:
        response = requests.get(url=item)
        print("Error Check Returned:")
        print(response.raise_for_status())
        print(response.status_code)
        if(response.status_code == 200):
            response = requests.get(url=item)
            json_TempData = json.loads(response.text)
            pprint.pprint(json_TempData)

    except requests.exceptions.HTTPError as err:
        print(err)



## Time comparision
print('\n')
created_at = json_data.get('created_at')
updated_at = json_data.get('updated_at')
# Convert time format
created = time.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
updated = time.strptime(updated_at, '%Y-%m-%dT%H:%M:%SZ')
print("Created: " + str(created_at))
print('\n')
print("Updated: " + str(updated_at))
print('\n')
created = time.mktime(created)
updated = time.mktime(updated)

if(updated-created) > 0:
    print("The updated time is greater than the created time")


## Verification of source JSON object
# Uses pagination request to call larger set
repos = requests.get(url='https://api.github.com/orgs/BoomTownROI/repos?page=1&per_page=100')
reposJson = repos.json()



print('\n')
print('\n')
# Retrieves public_repo value to compare
repoCount = json_data.get('public_repos')

print("Comparing public_repo to json counter..." + '\n')
if len(reposJson) == repoCount:
    print("Repo matches counter")
    print("public_repo: " + str(repoCount))
    print("repo_urls: " + str(len(reposJson)))
else:
    print("Repo does not equal counter.")
    print("public_repo: " + str(repoCount))
    print("repo_urls: " + str(len(reposJson)))
