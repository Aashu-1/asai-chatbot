---
title: AshAI Chatbot
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
---

# AshAI - AI Chatbot

An intelligent chatbot powered by Groq's LLaMA model with RAG (Retrieval Augmented Generation) capabilities.

## Features

- 🤖 AI-powered chat using Groq API
- 📄 PDF-based knowledge retrieval (RAG)
- 📧 Lead collection via email
- 💬 Conversational interface

## Setup

### Environment Variables

Add these secrets in your Hugging Face Space settings:

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key |
| `DOCUMENT_PATH` | URL to your PDF document |
| `EMAIL_USER` | Gmail address for sending emails |
| `EMAIL_PASS` | Gmail app password |
| `OWNER_EMAIL` | Email to receive leads |

### Getting a Groq API Key

1. Sign up at https://console.groq.com
2. Create an API key
3. Add it to your Space secrets

### Gmail App Password

1. Enable 2FA on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate an app password for "Mail"
4. Use this as `EMAIL_PASS`

## How It Works

1. The chatbot loads your PDF and creates embeddings
2. When you ask a question, it retrieves relevant context
3. Uses RAG to answer from your document
4. If info isn't available, collects user details and emails you
