import time
from azure.core.exceptions import ResourceNotFoundError
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

class ChunkIndexManager(IndexManager):

    def _create_chunk_index(self, index_prefix):
        name = get_index_name(f"{index_prefix}-chunk")
        vector_search = VectorSearch(
            algorithm_configurations=[
                VectorSearchAlgorithmConfiguration(
                    name="my-vector-config",
                    kind="hnsw",
                    hnsw_parameters={
                        "m": 4,
                        "efConstruction": 400,
                        "efSearch": 1000,
                        "metric": "cosine"
                    }
                )
            ]
        )
        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String,  filterable=True, sortable=True, key=True),            
            SimpleField(name="source_document_id", type=SearchFieldDataType.String),
            SearchableField(name="source_document_filepath", type=SearchFieldDataType.String,searchable=True),
            SimpleField(name="source_field_name", type=SearchFieldDataType.String),
            SearchableField(name="title", type=SearchFieldDataType.String, searchable=True),   
            SimpleField(name="index", type=SearchFieldDataType.Int64),
            SimpleField(name="offset", type=SearchFieldDataType.Int64),
            SimpleField(name="length", type=SearchFieldDataType.Int64),
            SimpleField(name="hash", type=SearchFieldDataType.String),
            SearchableField(name="text", type=SearchFieldDataType.String),                 
            SearchField(name="embedding", type=SearchFieldDataType.Collection(SearchFieldDataType.Single), searchable=True, vector_search_dimensions=1536, vector_search_configuration="my-vector-config")    
        ]
        index = self.create_index(name, fields, vector_search=vector_search, semantic_title_field_name="title", semantic_content_field_names=["text"])
        return index
    
    def _create_chunk_datasource(self, index_prefix, storage_connection_string, container_name):
        name = get_datasource_name(f"{index_prefix}-chunk")
        return self.create_blob_datasource(name, storage_connection_string, container_name)

    def _create_indexer(self, index_prefix, data_source_name, index_name):
        name = get_indexer_name(f"{index_prefix}-chunk")
        parameters = IndexingParameters(configuration={"parsing_mode": "json"})
        indexer = SearchIndexer(
            name=name,
            data_source_name=data_source_name,
            target_index_name=index_name,
            parameters=parameters
        )
        indexer_client = get_indexer_client()
        return indexer_client.create_indexer(indexer)
    


    def _create_chunk_indexer(self, index_prefix, data_source_name,index_name):
        print("creating indexer")
        indexer_name = self._create_indexer(index_prefix, data_source_name, index_name).name
        self.wait_for_indexer_completion(indexer_name)
        return indexer_name

    def create_chunk_index_resources(self, index_prefix, data_source_name=None,index_name=None,
                                     chunk_index_storage_connection_string = None,
                                     chunk_index_blob_container_name = None) -> dict:

        if data_source_name is None:
            data_source_name = self.data_source_name = self._create_chunk_datasource(index_prefix, chunk_index_storage_connection_string, chunk_index_blob_container_name).name 
        if index_name is None:
            index_name = self._create_chunk_index(index_prefix).name
        time.sleep(5)
        indexer_name =self._create_chunk_indexer(index_prefix, data_source_name,index_name)
        return {"index_name": index_name, "data_source_name": data_source_name, "indexer_name": indexer_name}


    # delete all the resources
    def delete_chunk_index_resources(self, index_prefix):
        index_client = get_index_client()
        indexer_client = get_indexer_client()

        index_client.delete_index(index=f"{index_prefix}-chunk-index")
        indexer_client.delete_indexer(indexer=f"{index_prefix}-chunk-indexer")
