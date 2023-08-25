import os
import sys
import time
import base64
from tabulate import tabulate
import json
from azure.core.serialization import AzureJSONEncoder
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import asyncio
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient 

async def get_all_files():
        # Create an API client with the credentials and scopes.

        client_id = "caba7ec5-785a-455e-adb1-a2ee299725f1"
        client_secret = "E0r8Q~qqlpPEGIrQIReDjs2O6LYeVsb~yOw4UbSZ"
        tenant = "6bf55bfe-0a0b-4ad2-9464-41a84e03d6ec"
        file_path = "/drives/b!nzlh62k8YUGpuOXDsJSmbTzNKa0SAjJEpOWEWtf15vk8xKlA9HLzTZv0pIxgyrqJ/root:/Abdul Latif/GBA_Office365_licenses_Quote_2016 (1).pdf"
        details = file_path.split('/')
        drive_id = details[2]
        folder_name = details[4]
        file_name = details[5] 

        # Create a credential object. Used to authenticate requests
        credential = ClientSecretCredential(
            tenant_id=tenant,
            client_id=client_id,
            client_secret=client_secret
        )
        scopes = ['https://graph.microsoft.com/.default']

        client = GraphServiceClient(credentials=credential, scopes=scopes)
        try:
            all_files = []
            folders = await client.drives.by_drive_id(drive_id).items.by_drive_item_id('root').children.get()
            if folders and folders.value:
                print("Retriving files from root directory")
                for folder in folders.value:
                    if folder:
                        folder_id = folder.id
                        items = await client.drives.by_drive_id(drive_id).items.by_drive_item_id(folder_id).children.get()
                        if items and items.value:
                            for item in items.value:
                                if item.name and '.pdf' in item.name:
                                    all_files.append(f"/drives/b!nzlh62k8YUGpuOXDsJSmbTzNKa0SAjJEpOWEWtf15vk8xKlA9HLzTZv0pIxgyrqJ/root:/{folder.name}/{item.name}")
                    else:
                        print("Folder not found")
                        return None
                return all_files
        except Exception as e:
            print("Error getting File URL")
            print(e)
            return None
all_files = asyncio.run(get_all_files())

print(f"Found {len(all_files)} pdf files" )
print(f"Calling the apis")
import requests

# Define the API endpoint
endpoint = "http://localhost:7071/api/chunk-embed"

# Create the request body
request_body = {
    "values": [
        {
            "recordId": "0",
            "data": {
                "document_id": "1",
                "fieldname": "field_name"
            }
        }
    ]
}
def loading_animation(iterable):
    animation = "|/-\\"
    for item in iterable:
        for char in animation:
            sys.stdout.write(f"\rLoading {char} {item}")
            sys.stdout.flush()
            time.sleep(0.1)

# Make API requests for each file path
for filepath in all_files:
    request_body["values"][0]["data"]["filepath"] = filepath
    response = requests.post(endpoint, json=request_body)
    
    if response.status_code == 200:
        print(f"API request successful for file: {filepath}")
    else:
        print(f"API request failed for file: {filepath}")
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
