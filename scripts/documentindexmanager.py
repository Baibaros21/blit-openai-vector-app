import time
import os
import openai
import requests
from langchain.embeddings import OpenAIEmbeddings
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
from importsandgetters import (get_index_name,
                               get_datasource_name,
                               get_skillset_name,
                               get_chunk_index_blob_container_name,
                               get_index_client,
                               get_indexer_client,
                               get_indexer_name,
                               get_knowledge_store_connection_string
                               )
from indexmanager import IndexManager
class DocumentIndexManager(IndexManager):
  
    def _create_document_index(self, index_prefix):
        
        name = "sharepoint-index" #get_index_name(index_prefix)
        fields = [
                    SimpleField(name="document_id", type=SearchFieldDataType.String, filterable=True, sortable=True, key=True),
                    SearchableField(name="content", type=SearchFieldDataType.String),
                    SimpleField(name="filesize", type=SearchFieldDataType.Int64),
                    SimpleField(name="filepath", type=SearchFieldDataType.String 
                                )
                ]
        return self.create_index(name, fields, vector_search=None, semantic_title_field_name="filepath", semantic_content_field_names=["content"]) 
    
    def _get_index(self, index_prefix):

        return "sharepoint-index"
            
    def _create_document_datasource(self, index_prefix, storage_connection_string, container_name):
        name = get_datasource_name(index_prefix)
        return self.create_blob_datasource(name, storage_connection_string, container_name)

    def _create_document_skillset(self, index_prefix, content_field_name="content"):


        name = "sharepoint-skillset"
        chunk_index_blob_container_name = get_chunk_index_blob_container_name(index_prefix)
        content_context = f"/document/{content_field_name}"
 
        embedding_skill = WebApiSkill(
                            name="chunking-embedding-skill",
                            uri=f"https://chunk-embed-function-app.azurewebsites.net/api/chunk-embed" ,
                            timeout="PT230S",
                            batch_size=1,
                            http_headers={"x-functions-key": "HdCOewX7wX6ex3D2HPZOMboT9l3oo6CS2zf0gqwCVAvIAzFultK-3Q=="},
                            degree_of_parallelism=3,
                            context=content_context,
                            inputs=[
                                    InputFieldMappingEntry(name="document_id", source="/document/document_id"),
                                    InputFieldMappingEntry(name="text", source=content_context),
                                    InputFieldMappingEntry(name="filepath", source="/document/filepath"),
                                    InputFieldMappingEntry(name="fieldname", source=f"='{content_field_name}'")],
                            outputs=[OutputFieldMappingEntry(name="chunks", target_name="chunks")])
        knowledge_store = SearchIndexerKnowledgeStore(storage_connection_string=get_knowledge_store_connection_string(),
                                                    projections=[
                                                                SearchIndexerKnowledgeStoreProjection(
                                                                    objects=[SearchIndexerKnowledgeStoreFileProjectionSelector(
                                                                        storage_container=chunk_index_blob_container_name,
                                                                        generated_key_name="id",
                                                                        source_context=f"{content_context}/chunks/*",
                                                                        inputs=[
                                                                            InputFieldMappingEntry(name="document_id", source="/document/document_id"),
                                                                            InputFieldMappingEntry(name="filepath", source="/document/filepath"),
                                                                            InputFieldMappingEntry(name="source_field_name", source=f"{content_context}/chunks/*/embedding_metadata/source_field_name"),
                                                                            InputFieldMappingEntry(name="title", source=f"{content_context}/chunks/*/title"),
                                                                            InputFieldMappingEntry(name="text", source=f"{content_context}/chunks/*/content"),
                                                                            InputFieldMappingEntry(name="embedding", source=f"{content_context}/chunks/*/embedding_metadata/embedding"),
                                                                            InputFieldMappingEntry(name="index", source=f"{content_context}/chunks/*/embedding_metadata/index"),
                                                                            InputFieldMappingEntry(name="offset", source=f"{content_context}/chunks/*/embedding_metadata/offset"),
                                                                            InputFieldMappingEntry(name="length", source=f"{content_context}/chunks/*/embedding_metadata/length")                                                                            
                                                                            ]
                                                                            )
                                                                    ])
                                                                ])
 
        skillset = SearchIndexerSkillset(name=name, skills=[embedding_skill], description=name,knowledge_store=knowledge_store)
        client = get_indexer_client()
        return client.create_skillset(skillset) 
    
    def _get_skillset(self, index_prefix):

        skillset_name = "sharepoint-skillset"

        return skillset_name

    def _create_document_indexer(self, index_prefix, data_source_name, index_name, skillset_name, content_field_name="content", generate_page_images=False):
        content_context = f"/document/{content_field_name}"
        name = get_indexer_name(index_prefix)
        indexer_config = {"dataToExtract": "contentAndMetadata","indexedFileNameExtensions" : ".pdf, .docx","excludedFileNameExtensions" : ".png, .jpg"}
        parameters = IndexingParameters(batch_size=100, max_failed_items = -1,configuration=indexer_config)
        indexer = SearchIndexer(
            name=name,
            target_index_name=index_name,
            data_source_name=data_source_name,
            skillset_name=skillset_name,
            field_mappings=[FieldMapping(source_field_name="metadata_spo_site_library_item_id", target_field_name="document_id", mapping_function=FieldMappingFunction(name="base64Encode", parameters=None)),
                            FieldMapping(source_field_name="metadata_spo_item_path", target_field_name="filepath"),
                            FieldMapping(source_field_name="metadata_spo_item_size", target_field_name="filesize")
                            ],
            output_field_mappings=[],
            parameters=parameters

        )
        indexer_client = get_indexer_client()
        return indexer_client.create_indexer(indexer) 
    
    def _create_document_datasource(self, index_prefix, storage_connection_string, container_name):
        name = get_datasource_name(index_prefix)
        return self.create_blob_datasource(name, storage_connection_string, container_name) 
    
    def _get_datasource(self, index_prefix):
      
        data_source_name = "sharepoint-datasource"

        return  data_source_name
    

    def _get_indexer(self, index_prefix):
        indexer_name = 'sharepoint-indexer'
        return indexer_name

    def create_document_indexer(self, index_prefix) -> dict:
            index_name = self._get_index(index_prefix)
            data_source_name = self._get_datasource(index_prefix)
            skillset_name = self._get_skillset(index_prefix)
            time.sleep(5)
            indexer_name = self._create_document_indexer(index_prefix,data_source_name,index_name,skillset_name)
            return {"index_name": index_name, 
                    "data_source_name": data_source_name,
                      "skillset_name": skillset_name, 
                      "indexer_name": indexer_name}  
    
    def create_document_index_resources(self, index_prefix) -> dict:
            index_name = self._create_document_index(index_prefix)
            data_source_name = self._get_datasource(index_prefix)
            skillset_name = self._create_document_skillset(index_prefix)
            time.sleep(5)
            indexer_name = self._create_document_indexer(index_prefix,data_source_name,index_name,skillset_name)
            return {"index_name": index_name, 
                    "data_source_name": data_source_name,
                      "skillset_name": skillset_name, 
                      "indexer_name": indexer_name}  
    def create_document_indexer_and_skillset(self,index_prefix):
        index_name = self._get_index(index_prefix)
        data_source_name = self._get_datasource(index_prefix)
        skillset_name = self._create_document_skillset(index_prefix)
        time.sleep(5)
        indexer_name = self._create_document_indexer(index_prefix,data_source_name,index_name,skillset_name)
        return {"index_name": index_name, 
                "data_source_name": data_source_name,
                    "skillset_name": skillset_name, 
                    "indexer_name": indexer_name}  
         
    def create_index_and_skillset(self,index_prefix):
        index_name = self._create_document_index(index_prefix)
        skillset_name = self._create_document_skillset(index_prefix)

        return {"index_name": index_name, 
        
            "skillset_name": skillset_name, 
            } 
          
    




    def delete_document_index_resources(self, index_prefix):
        index_client = get_index_client()
        indexer_client = get_indexer_client()

        index_client.delete_index("sharepoint-index")
        indexer_client.delete_skillset("sharepoint-skillset")
        indexer_client.delete_indexer(indexer=get_indexer_name(index_prefix))

        # indexer_client.delete_data_source_connection(data_source_connection=get_datasource_name(index_prefix))
        # indexer_client.delete_skillset(skillset=get_skillset_name(index_prefix))

        # # delete the knowledge store tables and blobs
        # knowledge_store_connection_string  = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        
        # # delete the container directly from storage
        # try:
        #     blob_service = BlobServiceClient.from_connection_string(knowledge_store_connection_string)
        #     blob_service.delete_container(get_chunk_index_blob_container_name(index_prefix))
        # # handle resource not found error
        # except ResourceNotFoundError:
        #     pass