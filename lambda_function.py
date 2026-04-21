import json
import boto3
import math
import anthropic


def lambda_handler(event, context):
    print("Function started")
    body = json.loads(event['body'])
    query = body['query']
    print("Query received:", query)
    
    bedrock = boto3.client('bedrock-runtime', region_name='eu-west-2')
    s3 = boto3.client('s3', region_name='eu-west-2')
    print("Clients created")
    
    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v2:0',
        body=json.dumps({'inputText': query})
    )
    print("Bedrock embedding done")

def lambda_handler(event, context):
    body = json.loads(event['body'])
    query = body['query']
    
    bedrock = boto3.client('bedrock-runtime', region_name='eu-west-2')
    s3 = boto3.client('s3', region_name='eu-west-2')
    
    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v2:0',
        body=json.dumps({'inputText': query})
    )
    result = json.loads(response['body'].read())
    query_embedding = result['embedding']
    
    kb_object = s3.get_object(Bucket='runbook-assistant-amaan', Key='knowledge_base.json')
    knowledge_base = json.loads(kb_object['Body'].read())
    
    def cosine_similarity(a, b):
        dot = sum(x*y for x,y in zip(a,b))
        mag_a = math.sqrt(sum(x*x for x in a))
        mag_b = math.sqrt(sum(x*x for x in b))
        return dot / (mag_a * mag_b)
    
    scored = []
    for chunk in knowledge_base:
        score = cosine_similarity(query_embedding, chunk['embedding'])
        scored.append((score, chunk['text']))
    
    scored.sort(reverse=True)
    top_chunks = [text for _, text in scored[:3]]
    context_text = '\n\n'.join(top_chunks)
    
    
    import os
    client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
    message = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=1000,
        messages=[{
            'role': 'user',
            'content': f'Answer this question using only the context below.\n\nContext:\n{context_text}\n\nQuestion: {query}'
        }]
    )
    
    answer = message.content[0].text
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'answer': answer})
    }