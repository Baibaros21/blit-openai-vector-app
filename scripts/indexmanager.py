import requests
import os
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

from importsandgetters import (get_index_name,
                               get_datasource_name,
                               get_skillset_name,
                               get_chunk_index_blob_container_name,
                               get_index_client,
                               get_indexer_client,
                               get_indexer_name
                               )
class IndexManager():
     def create_index(self,index_name, fields, vector_search, semantic_title_field_name, semantic_content_field_names):
        semantic_settings = SemanticSettings(
            configurations=[SemanticConfiguration(
                name='default',
                prioritized_fields=PrioritizedFields(
                    title_field=SemanticField(field_name=semantic_title_field_name), prioritized_content_fields=[SemanticField(field_name=field_name) for field_name in semantic_content_field_names]))])
        index = SearchIndex(
            name=index_name,
            fields=fields,
            vector_search=vector_search,
            semantic_settings=semantic_settings)
        index_client = get_index_client()
        return index_client.create_index(index) 
       
     
     def create_blob_datasource(self,datasource_name, storage_connection_string, container_name):
    # This example utilizes a REST request as the python SDK doesn't support the blob soft delete policy yet
        AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")
        AZURE_SEARCH_SERVICE_ENDPOINT =os.environ.get("AZURE_SEARCH_SERVICE_ENDPOINT")
        api_version = '2023-07-01-Preview'
        headers = {
            'Content-Type': 'application/json',
            'api-key': f'{AZURE_SEARCH_KEY}'
        }
        data_source = {
            "name": datasource_name,
            "type": "azureblob",
            "credentials": {"connectionString": storage_connection_string},
            "container": {"name": container_name},
            "dataDeletionDetectionPolicy": {"@odata.type": "#Microsoft.Azure.Search.NativeBlobSoftDeleteDeletionDetectionPolicy"}
        }

        url = '{}/datasources/{}?api-version={}'.format(AZURE_SEARCH_SERVICE_ENDPOINT, datasource_name, api_version)
        response = requests.put(url, json=data_source, headers=headers)

        ds_client = get_indexer_client()
        return ds_client.get_data_source_connection(datasource_name)
    
     def wait_for_indexer_completion(self,indexer_name):
        indexer_client = get_indexer_client()
        # poll status and wait until indexer is complete
        status = f"Indexer {indexer_name} not started yet"
        while (indexer_client.get_indexer_status(indexer_name).last_result == None) or ((status := indexer_client.get_indexer_status(indexer_name).last_result.status) != "success"):
            print(f"Indexing status:{status}")

            # It's possible that the indexer may reach a state of transient failure, especially when generating embeddings
            # via Open AI. For the purposes of the demo, we'll just break out of the loop and continue with the rest of the steps.
            if (status == "transientFailure"):
                print(f"Indexer {indexer_name} failed before fully indexing documents")
                break