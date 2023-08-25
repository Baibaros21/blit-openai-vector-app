import os
from dotenv import load_dotenv


# # Open the .env file in append mode
# # with open(".env", "a") as env_file:
# #     # Write the new environment variable in the format 'KEY=VALUE\n'
# #     env_file.write("DB_HOST=new_value\n")
# #     env_file.write("AZURE_SEARCH_INDEX=blitopenaiindex\n")
# #     env_file.write("AZURE_SEARCH_SERVICE=blitopenaisearch\n")
# #     env_file.write("AZURE_SEARCH_KEY=HqPgRP2f6kjijYKloQFATaPrLcb8r10xu21yoa4JbyAzSeA7S8EU\n")
# #     env_file.write("AZURE_SEARCH_USE_SEMANTIC_SEARCH=False\n")
# #     env_file.write("AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG=default\n")
# #     env_file.write("AZURE_SEARCH_INDEX_IS_PRECHUNKED=False\n")
# #     env_file.write("AZURE_SEARCH_TOP_K=5\n")
# #     env_file.write("AZURE_SEARCH_ENABLE_IN_DOMAIN=False\n")
# #     env_file.write("AZURE_SEARCH_CONTENT_COLUMNS=\n")
# #     env_file.write("AZURE_SEARCH_FILENAME_COLUMN=\n")
# #     env_file.write("AZURE_SEARCH_TITLE_COLUMN=\n")
# #     env_file.write("AZURE_SEARCH_URL_COLUMN=\n")
# #     env_file.write("AZURE_OPENAI_RESOURCE=blit-openaiservice\n")
# #     env_file.write("AZURE_OPENAI_MODEL=BLIT-gpt3\n")
# #     env_file.write("AZURE_OPENAI_KEY=3046815f23344bff9d76e3b7c36a79a9\n")
# #     env_file.write("AZURE_OPENAI_MODEL_NAME=gpt-35-turbo\n")
# #     env_file.write("AZURE_OPENAI_TEMPERATURE=0\n")
# #     env_file.write("AZURE_OPENAI_TOP_P=1.0\n")
# #     env_file.write("AZURE_OPENAI_MAX_TOKENS=1000\n")
# #     env_file.write("AZURE_OPENAI_STOP_SEQUENCE=\n")
# #     env_file.write("AZURE_OPENAI_SYSTEM_MESSAGE=You are an AI assistant that helps people find information.\n")
# #     env_file.write("AZURE_OPENAI_PREVIEW_API_VERSION=2023-06-01-preview\n")
# #     env_file.write("AZURE_OPENAI_STREAM=True\n")

# os.environ['AZURE_OPENAI_EMBEDDING_MODEL']='BLIT-ada002'

# load_dotenv()

# # # ACS Integration Settings
# # AZURE_SEARCH_SERVICE = os.environ.get("AZURE_SEARCH_SERVICE")
# # AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")
# # AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")

# TEST = os.environ.get("AZURE_OPENAI_EMBEDDING_MODEL")
# print(TEST)
# # print(AZURE_SEARCH_INDEX,AZURE_SEARCH_KEY) 
load_dotenv()
AZURE_SEARCH_SERVICE_ENDPOINT = os.environ.get("AZURE_SEARCH_SERVICE_ENDPOINT")
AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")
AZURE_SEARCH_KNOWLEDGE_STORE_CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
