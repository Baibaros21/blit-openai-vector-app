import os
import re
import sys
import openai
import requests
from flask import Response
import json
from dotenv import load_dotenv
from azure.search.documents.models import Vector  
from azure.search.documents import SearchClient  
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes.models import (
  SearchIndex,  
    SearchField,  
    SearchFieldDataType,  
    SimpleField,  
    SearchableField,  
    SearchIndex,  
    SemanticConfiguration,  
    PrioritizedFields,  
    SemanticField,  
    SearchField,  
    SemanticSettings,  
    VectorSearch,  
    VectorSearchAlgorithmConfiguration,  
)
load_dotenv()
AZURE_OPENAI_EMBEDDING_MODEL=os.environ.get("AZURE_OPENAI_EMBEDDING_MODEL")
AZURE_OPENAI_RESOURCE=os.environ.get("AZURE_OPENAI_RESOURCE")
API_KEY=os.environ.get("AZURE_OPENAI_KEY")
AZURE_SEARCH_SERVICE_ENDPOINT=os.environ.get("AZURE_SEARCH_SERVICE_ENDPOINT")
AZURE_SEARCH_KEY=os.environ.get("AZURE_SEARCH_KEY")
AZURE_SEARCH_SHAREPOINT_INDEX="sharepoint-index"
RESOURCE_ENDPOINT = f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/openai/deployments/{AZURE_OPENAI_EMBEDDING_MODEL}/embeddings?api-version=2023-03-15-preview" 
AZURE_STORAGE_CONNECTION_STRING=os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER_NAME=os.environ.get('AZURE_STORAGE_CONTAINER_NAME') 
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
from vectorsearchmanager import VectorSearchManager

search_manager = VectorSearchManager("blit-openai-vector")
print(search_manager.create_doc_indexes())
# search_manager.delete_indexes()
# print("indexes deleted!")


# search_manager.get_chunk_index_resources() 
# search_manager.get_chunk_vector_search("blit-openai-vector-chunk-index","Project Manager",True,1) 



