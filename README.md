# AWS RAG Runbook Assistant

A small proof‑of‑concept project that demonstrates how to build a
document question‑answering system on AWS using serverless services
and large language models.

## Overview
The system allows a user to ask operational questions and receive
answers grounded in real AWS documentation (runbooks and
troubleshooting guides).

Documents are embedded ahead of time and stored. At query time,
relevant sections are retrieved and provided to an LLM to generate
the response.

## Architecture
- Frontend: Static HTML + JavaScript
- API: Amazon API Gateway
- Backend: AWS Lambda (Python)
- Embeddings: Amazon Bedrock (Titan)
- Storage: Amazon S3
- Language model: Claude (via API)

Flow:
User → API Gateway → Lambda → embedding + retrieval → LLM → response

## Purpose
The goal of this project was to understand how retrieval‑augmented
generation systems are built and deployed using AWS services,
rather than to create a production‑ready application.

## Current state
- End‑to‑end pipeline implemented
- Serverless and minimal infrastructure
- Intended as a learning and demonstration project

## Possible next steps
- Use a dedicated vector database
- Add authentication and access control
- Improve ingestion and document updates
- Add basic monitoring and logging

Built as a learning project for AWS Summit London.
