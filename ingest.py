import os
import json
import boto3
import json


print("Script started")

def load_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r') as f:
                text = f.read()
                documents.append({'filename': filename, 'text': text})
    return documents

def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    for word in words:
        current_chunk.append(word)
        current_length += 1
        if current_length >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_length = 0
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks


def embed_chunks(chunks):
    bedrock = boto3.client('bedrock-runtime', region_name='eu-west-2')
    embedded = []
    for chunk in chunks:
        response = bedrock.invoke_model(
            modelId='amazon.titan-embed-text-v2:0',
            body=json.dumps({'inputText': chunk})
        )
        result = json.loads(response['body'].read())
        embedding = result['embedding']
        embedded.append({'text': chunk, 'embedding': embedding})
        print(f"Embedded chunk of {len(chunk.split())} words")
    return embedded

def save_to_s3(embedded_chunks, bucket_name):
    s3 = boto3.client('s3', region_name='eu-west-2')
    data = json.dumps(embedded_chunks)
    s3.put_object(
        Bucket=bucket_name,
        Key='knowledge_base.json',
        Body=data
    )
    print(f"Saved {len(embedded_chunks)} chunks to S3")

docs = load_documents('documents')
all_embedded_chunks = []
for doc in docs:
    chunks = chunk_text(doc['text'])
    print(f"{doc['filename']}: {len(chunks)} chunks")
    embedded = embed_chunks(chunks)
    all_embedded_chunks.extend(embedded)

save_to_s3(all_embedded_chunks, 'runbook-assistant-amaan')