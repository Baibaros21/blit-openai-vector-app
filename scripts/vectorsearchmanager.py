import importsandgetters
import os
import time
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from azure.search.documents.models import Vector  
from azure.search.documents import SearchClient  
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from documentindexmanager import DocumentIndexManager
from textembedder import TextEmbedder
from chunkindexmanager import ChunkIndexManager
class VectorSearchManager():

    def __init__(self,prefix) -> None:

        self.index_resources= None
        self.prefix = prefix
        self.storage_connection_string = "SharePointOnlineEndpoint=https://blueridgeitfze.sharepoint.com;ApplicationId=df79b7a3-30bf-4032-bc98-cd486088a572;"
        self.doc_container_name = os.environ.get("AZURE_STORAGE_DOC_CONTAINER_NAME") 
        self.chunk_container_name = os.environ.get("AZURE_STORAGE_CHUNK_CONTAINER_NAME")

        pass

    def _create_indexes(self):
        index_manager = DocumentIndexManager()
        doc_index_resources = index_manager.create_document_index_resources(
            self.prefix, self.storage_connection_string, self.doc_container_name)
        
        print("Document index resources created")

        time.sleep(5)

        chunk_index_manager = ChunkIndexManager()
        chunk_index_resources = chunk_index_manager.create_chunk_index_resources(self.prefix,
                                                                                 self.storage_connection_string,
                                                                                  self.chunk_container_name)
        print("chunk index resources created")

        print(doc_index_resources,chunk_index_resources)
        return {"doc_index_resources": doc_index_resources, "chunk_index_resources": chunk_index_resources}
    
    def create_doc_indexes(self):
        index_manager = DocumentIndexManager()
        doc_index_resources = index_manager.create_document_index_resources(
        self.prefix)
        
        print("Document index resources created")
        print(doc_index_resources) 

    def creat_doc_indexer(self):
        index_manager = DocumentIndexManager()
        doc_index_resources = index_manager.create_document_indexer(
        self.prefix)
        
        print("Document indexer resources created")
        print(doc_index_resources)  

    def create_doc_indexer_skillset(self):

        index_manager = DocumentIndexManager()
        doc_index_resources = index_manager.create_document_indexer_and_skillset(self.prefix)
        
        print("Document indexer resources created")
        print(doc_index_resources)  






    def create_doc_index(self):
        index_manager = DocumentIndexManager()
        return index_manager._get_index(self.prefix)
    
    def create_doc_index_and_skillset(self):
        index_manager = DocumentIndexManager()
        return index_manager.create_index_and_skillset(self.prefix)

    def delete_indexes(self):
        index_manager = DocumentIndexManager()
        index_manager.delete_document_index_resources(self.prefix)
        chunk_index_manager = ChunkIndexManager()
        chunk_index_manager.delete_chunk_index_resources(self.prefix)
    def delete_doc_indexes(self):
        index_manager = DocumentIndexManager()
        index_manager.delete_document_index_resources(self.prefix)


    def _query_vector_index(self,index_name, query, vector_only=False,top_k=3):
        AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")
        AZURE_SEARCH_SERVICE_ENDPOINT =os.environ.get("AZURE_SEARCH_SERVICE_ENDPOINT")
        embedder = TextEmbedder()
        vector = embedder.generate_embeddings(query)
        search_client = SearchClient(AZURE_SEARCH_SERVICE_ENDPOINT, index_name, AzureKeyCredential(AZURE_SEARCH_KEY)) 
        if vector_only:
            search_text = None
        else:
            search_text = query
        results = search_client.search(search_text=search_text, vector=vector, vector_fields="embedding", top_k=top_k)
        return results 
    
    def _get_indexes(self):
        if self.index_resources is None:
            print("Creating the indexes")
            self.index_resources = self._create_indexes()
        return self.index_resources
    
    def _get_doc_index_resources(self):
        print("Getting doc index")
        return self._get_indexes()["doc_index_resources"]["index_name"]
    def _get_chunk_index_resources(self):
        print("Getting Chunk index")
        return self._get_indexes()["chunk_index_resources"]["index_name"]
    

    def get_chunk_vector_search(self,chunk_index_name,query,vector_only=False,top_k=3):
        results = self._query_vector_index(index_name=chunk_index_name, query=query, vector_only=vector_only,top_k=top_k)
        
        for result in results:
            print(f"Title: {result['title']}")  
            print(f"Content: {result['text']}")  
            print(f"Source Document: {result['source_document_filepath']}")  


    