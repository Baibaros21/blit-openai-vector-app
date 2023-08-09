import openai
import os
class TextEmbedder():
    openai.api_type = "azure"    
    openai.api_key = os.getenv("AZURE_OPENAI_KEY")
    openai.api_base = f"https://{os.getenv('AZURE_OPENAI_RESOURCE')}.openai.azure.com/"
    openai.api_version = os.getenv("AZURE_OPENAI_PREVIEW_API_VERSION")
    AZURE_OPENAI_EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")

    # def clean_text(self, text, text_limit=7000):
    #     # Clean up text (e.g. line breaks, )    
    #     text = re.sub(r'\s+', ' ', text).strip()
    #     text = re.sub(r'[\n\r]+', ' ', text).strip()
    #     # Truncate text if necessary (e.g. for, ada-002, 4095 tokens ~ 7000 chracters)    
    #     if len(text) > text_limit:
    #         logging.warning("Token limit reached exceeded maximum length, truncating...")
    #         text = text[:text_limit]
    #     return text

    # Function to generate embeddings for title and content fields, also used for query embeddings
    def generate_embeddings(self, text, clean_text=True):
        # if clean_text:
        #     text = self.clean_text(text)
        response = openai.Embedding.create(input=text, engine=self.AZURE_OPENAI_EMBEDDING_MODEL)
        embeddings = response['data'][0]['embedding']
        return embeddings