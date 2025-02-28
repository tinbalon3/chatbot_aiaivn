import os
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models
import openai
from dotenv import load_dotenv
# Thiết lập API key của OpenAI
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

qdrant_client = QdrantClient("localhost", port=6333)


def create_collection():
    
    if qdrant_client.collection_exists("chatbot_data"):
        print("Collection 'chatbot_data' already exists!")
    else:
        qdrant_client.create_collection(
        collection_name="chatbot_data",
        vectors_config=models.VectorParams(
            size=1536,
            distance=models.Distance.COSINE
        )
    )

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


def add_data_to_qdrant():
    texts = []
    with open("html_extracted.txt", "r", encoding="utf-8") as f:
        for line in f:
            text = line.strip()
            texts.append(text)
    vectors = [get_embedding(text) for text in texts]
    ids = list(range(len(texts)))
    
    qdrant_client.upsert(
        collection_name="chatbot_data",
        points=models.Batch(
            ids=ids,
            vectors=vectors,
            payloads=[{"text": text} for text in texts]
        )
    )
    print("Data added to Qdrant!")


def search_qdrant(query_text):
    query_vector = get_embedding(query_text)
    search_result = qdrant_client.search(
        collection_name="chatbot_data",
        query_vector=query_vector,
        limit=3  
    )
    return search_result


def summarize_results(results,query):

    combined_text = "\n".join([result.payload["text"] for result in results])
   
    prompt = (
        f"Câu hỏi của người dùng: '{query}'. "
        f"Nếu không có thông tin phù hợp trong dữ liệu sau, trả lời 'Không tìm thấy thông tin phù hợp'. "
        f"Nếu có, tóm tắt ngắn gọn và đúng trọng tâm:\n{combined_text}"
    )
 
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "Bạn là một trợ lý tóm tắt thông tin."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=500,  
    )
    
    summary = response.choices[0].message.content
    return summary


def chatbot(query):
    results = search_qdrant(query)
    if not results:
        return "Không tìm thấy thông tin phù hợp."
    

    summary = summarize_results(results,query)
    return summary


def initialize_data():
 
    create_collection()

    add_data_to_qdrant()

   