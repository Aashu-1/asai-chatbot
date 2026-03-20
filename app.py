import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
import os
from chroma_db import retrieve_context
from pdf_chunk import load_resume, chunk_text
from embeddings import embed_chunks
from chroma_db import store_in_chroma
from tools import tools
from send_email import send_email_to_owner

# ----------------------------
# LOAD ENV
# ----------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DOCUMENT_PATH = os.getenv("DOCUMENT_PATH", "")

# For Hugging Face Spaces - use persistent storage
HF_SPACE_ID = os.getenv("HF_SPACE_ID")
if HF_SPACE_ID:
    PERSIST_DIR = "/tmp/chroma_db"
else:
    PERSIST_DIR = "./chroma_db"

client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")


# ----------------------------
# LOAD RESUME
# ----------------------------
resume = None
chunks = []
if DOCUMENT_PATH:
    try:
        resume = load_resume(DOCUMENT_PATH)
        chunks = chunk_text(resume)
        embeddings = embed_chunks(chunks)
        store_in_chroma(chunks, embeddings)
    except Exception as e:
        print(f"Failed to load resume: {e}")



def collect_user_info(name, email, query):
    
    success = send_email_to_owner(name, email, query)

    if success:
        return f"User info collected successfully for {name}"
    else:
        return "Failed to send email"

# ----------------------------
# LLM FUNCTION
# ----------------------------
def chat_with_ai(message, history):
    history = history[-10:] if history else []

    messages = []

    for msg in history:
        messages.append({
            "role": msg.get("role"),
            "content": msg.get("content")
        })

    # 🔥 RAG CONTEXT
    context = retrieve_context(message,embed_chunks)
    print("🔍 Query:", message)
    print("📄 Retrieved Context:", context[:200])

    if not context:
        context = "No relevant information found in resume."

    system_prompt = f"""
You are AshAI — a smart AI assistant representing Aashutosh Chouhan.

Your job:
- if user greets, introduce yourself
- Answer questions ONLY using the provided context
- Be helpful, sharp, and slightly witty

STRICT RULES:
- DO NOT make up information
- If answer is in context → answer normally (short + emojis)
- If NOT in context:
    → DO NOT guess
    → Ask for name and email first
    → DO NOT call any function yet

LEAD CAPTURE FLOW:
- ONLY after user provides BOTH name AND email:
    → Call the function collect_user_info
    → Include actual values (no empty fields)
- NEVER call function with empty or missing fields

    IMPORTANT:
- Once user provides name and email → call the function `collect_user_info`
- Tell them you will forward their query to Aashutosh firmly 
- Once forwarded, inform the user
- NEVER fake tool calls
- NEVER answer without context

TONE:
- Friendly
- Slightly clever (not robotic)
- Professional but human

Context:
{context}
"""

    messages.insert(0, {"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": message})

    fresponse = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )   

    msg = fresponse.choices[0].message

    # 🔥 TOOL CALL HANDLING
    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        function_name = tool_call.function.name

        arguments = eval(tool_call.function.arguments)

        if function_name == "collect_user_info":
            if not arguments["name"] or not arguments["email"]:
                 return "Nice try 😄 but I still need both your name and email before I pass this along."
            result = collect_user_info(
                arguments["name"],
                arguments["email"],
                arguments["query"]
            )

            # Append tool result
            messages.append(msg)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

            # 🔁 Second LLM call (final response)
            final_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages
            )

            return final_response.choices[0].message.content

    return msg.content

# ----------------------------
# RESPONSE HANDLER
# ----------------------------
def respond(message, chat_history):
    if chat_history is None:
        chat_history = []

    response = chat_with_ai(message, chat_history)

    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": response})

    return "", chat_history


# ----------------------------
# UI
# ----------------------------
with gr.Blocks(title="AshAI Chatbot") as demo:
    gr.Markdown("# 🤖 AshAI\nPowered by Groq ⚡")
    
    with gr.Row():
        with gr.Column():
            chatbot = gr.Chatbot(height=500, type="messages")
            with gr.Row():
                msg = gr.Textbox(placeholder="Ask me anything...", scale=7)
                clear = gr.Button("Clear")
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(fn=lambda: ([], ""), outputs=[chatbot, msg])