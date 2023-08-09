import os
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
AZURE_SEARCH_SERVICE_ENDPOINT ="https://blitopenaisearch.search.windows.net"
AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX =  os.environ.get("AZURE_SEARCH_INDEX")

print(AZURE_SEARCH_KEY)




# Create a search index
index_client = SearchIndexClient(
    endpoint=AZURE_SEARCH_SERVICE_ENDPOINT, credential=AzureKeyCredential(AZURE_SEARCH_KEY)) 

# Retrieve existing index definition if the index exists
existing_index = index_client.get_index(AZURE_SEARCH_INDEX)


# Include existing fields from the retrieved index definition
existing_fields = existing_index.fields if existing_index else []

print(existing_fields)
new_fields = [
    # SimpleField(name="id", type=SearchFieldDataType.String, key=False, sortable=True, filterable=True, facetable=True),
    SearchField(name="contentVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True, vector_search_dimensions=1536, vector_search_configuration="my-vector-config"),
]
fields =existing_fields+new_fields
vector_search = VectorSearch(
    algorithm_configurations=[
        VectorSearchAlgorithmConfiguration(
            name="my-vector-config",
            kind="hnsw",
            hnsw_parameters={
                "m": 4,
                "efConstruction": 400,
                "efSearch": 500,
                "metric": "cosine"
            }
        )
    ]
)

semantic_config = SemanticConfiguration(
    name="my-semantic-config",
    prioritized_fields=PrioritizedFields(
                prioritized_content_fields=[SemanticField(field_name="content")]
    )
)

# Create the semantic settings with the configuration
semantic_settings = SemanticSettings(configurations=[semantic_config])

# Create the search index with the semantic settings
index = SearchIndex(name=AZURE_SEARCH_INDEX, fields=fields,
                    vector_search=vector_search, semantic_settings=semantic_settings)
result = index_client.create_or_update_index(index)
print(f' {result.name} created')