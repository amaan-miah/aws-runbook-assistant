# AWS RAG Runbook Assistant

A simple **Retrieval-Augmented Generation (RAG)** chatbot built on AWS that answers operational questions using real AWS documentation (runbooks).

## What it does
- Takes AWS runbook / troubleshooting documents
- Embeds them once and stores them
- Lets a user ask questions via a web UI
- Retrieves relevant document chunks
- Uses an LLM to generate grounded answers (no hallucinations)

## Architecture
- **Frontend:** Static HTML + JavaScript
- **API:** Amazon API Gateway
- **Backend:** AWS Lambda (Python)
- **Embeddings:** Amazon Bedrock (Titan)
- **Storage:** Amazon S3
- **LLM:** Claude (via API)

Flow:
User → API Gateway → Lambda → Bedrock embeddings → S3 retrieval → LLM → Response

## Why this project
Internal documentation is hard to search during incidents.  
This project is a proof‑of‑concept **internal runbook assistant** for cloud / DevOps teams.

## Status
- ✅ End‑to‑end pipeline working
- ✅ Serverless, minimal infrastructure
- ⚠️ Proof of concept (not production‑hardened)

## Future improvements
- Vector database instead of S3
- Authentication
- Event‑driven document ingestion
- Better UI

## Notes
Built as a learning project for AWS Summit London.
