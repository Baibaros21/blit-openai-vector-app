import os 
import time
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from azure.search.documents.models import Vector  
from azure.search.documents import SearchClient  
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (
    SimpleField,
    SearchField,
    SearchableField,
    SearchFieldDataType,
    SearchIndexer,
    IndexingParameters,
    FieldMapping,
    FieldMappingFunction,
    InputFieldMappingEntry, 
    OutputFieldMappingEntry, 
    SearchIndexerSkillset,
    SearchIndexerKnowledgeStore,
    SearchIndexerKnowledgeStoreProjection,
    SearchIndexerKnowledgeStoreFileProjectionSelector,
    IndexingParameters, 
    WebApiSkill,
    SearchIndex,
    SemanticSettings,
    SemanticConfiguration,
    PrioritizedFields,
    SemanticField,
    VectorSearch,  
    VectorSearchAlgorithmConfiguration
) 


AZURE_SEARCH_SERVICE_ENDPOINT = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_KNOWLEDGE_STORE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_SEARCH_KNOWLEDGE_STORE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CHUNK_CONTAINER_NAME")
def get_index_client() -> SearchIndexClient:
        return SearchIndexClient(AZURE_SEARCH_SERVICE_ENDPOINT, AzureKeyCredential(AZURE_SEARCH_KEY))

def get_indexer_client() -> SearchIndexerClient:
    return SearchIndexerClient(AZURE_SEARCH_SERVICE_ENDPOINT, AzureKeyCredential(AZURE_SEARCH_KEY))

def get_index_name(index_prefix):
    return f"{index_prefix}-index"

def get_datasource_name(index_prefix):
    return f"{index_prefix}-datasource"

def get_skillset_name(index_prefix):
    return f"{index_prefix}-skillset"

def get_indexer_name(index_prefix):
    return f"{index_prefix}-indexer"

def get_chunk_index_blob_container_name(index_prefix):
    return AZURE_SEARCH_KNOWLEDGE_STORE_CONTAINER_NAME

def get_knowledge_store_connection_string():
    return "DefaultEndpointsProtocol=https;AccountName=blitdocopenaistorage;AccountKey=v/TrgCrXhp9EEZaCIC+HbrSVOK7R+KUqQaC/ODqrpLAYxwGvdxygEAuM/MPnLQQWhB8jLzNRqM7w+AStl++19A==;EndpointSuffix=core.windows.net" 