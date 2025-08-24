import os
import traceback
from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from langchain.chat_models import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

try:
    vectorstore = FAISS.load_local(
        "malicious_vectorstore1",
        embeddings=OllamaEmbeddings(),
        allow_dangerous_deserialization=True
    )
    print("[+] Vector store loaded successfully.")
except Exception as e:
    print("[!] Error loading FAISS vector store:", e)
    traceback.print_exc()  # Print the full traceback for debugging
    exit(1)

# 🧠 Memory to keep chat history
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 💬 Local LLM via Ollama (make sure it's running)
try:
    llm = ChatOllama(
        model="llama2",  
        temperature=0
    )
    print("[+] Ollama model loaded successfully.")
except Exception as e:
    print("[!] Error loading Ollama model:", e)
    traceback.print_exc()  # Print the full traceback for debugging
    exit(1)

# 🔗 Retrieval-based QA chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    memory=memory,
    verbose=True
)

# 🗨️ Main user interaction loop
print("\n===  AI Support Agent (Powered by Ollama + FAISS ) ===")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print(" Goodbye.")
        break

    try:
        print(f"[DEBUG] Running query: {user_input}")
        response = qa_chain.invoke(user_input)  # Use invoke() instead of run()
        print("Assistant:", response)
    except Exception as e:
        print("[!] Error while running query:")
        traceback.print_exc()  # Print the full traceback for debugging
