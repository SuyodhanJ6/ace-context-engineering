# ACE Context Engineering

[![PyPI version](https://badge.fury.io/py/ace-context-engineering.svg)](https://badge.fury.io/py/ace-context-engineering)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Self-improving AI agents through evolving playbooks.** Use ACE as a **Context Provider** for any LLM framework (LangChain, OpenAI, etc.) to enable learning from experience without fine-tuning.

 **Based on research:** [Agentic Context Engineering (Stanford/SambaNova, 2025)](http://arxiv.org/pdf/2510.04618)

---

##  What is ACE?

ACE enables AI agents to **learn and improve** by accumulating strategies in a "playbook" - a knowledge base that grows smarter with each interaction. It now acts as a non-invasive **Context Provider**, giving you full control over your prompts while handling the heavy lifting of context retrieval and feedback analysis in the background.

### Key Benefits

-  **Developer Control**: Explicitly fetch context and inject it into your own prompts.
-  **Azure OpenAI Support**: Native support for Azure deployments including custom credentials.
-  **Non-Blocking Feedback**: Feedback analysis runs in background threads, keeping your app fast.
-  **Framework Agnostic**: Works with LangChain, raw OpenAI SDK, Anthropic, or any other LLM client.

---

##  Installation

### Using pip
```bash
# Default (FAISS vector store)
pip install ace-context-engineering

# With Azure OpenAI & LangChain Support
pip install ace-context-engineering[openai,langchain]
```

### Using uv (Recommended)
```bash
# Default (FAISS vector store)
uv add ace-context-engineering

# With full support
uv add ace-context-engineering[openai,langchain]
```

**Environment Setup:**

```bash
# Add your API keys to .env
echo "OPENAI_API_KEY=your-key-here" >> .env
```

---

##  Quick Start (ACE as Context Provider)

ACE is designed to be non-invasive. You fetch context, inject it into your prompt, and submit feedback later.

### 4-Step Integration

```python
from ace import ACEClient
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Initialize ACE Client
ace = ACEClient(playbook_name="my_app", vector_store="faiss")

# 2. Fetch context based on user query
user_query = "Process payment for order #12345"
context_string, interaction_id = ace.get_context(user_query)

# 3. Inject context into your own LLM call
llm = ChatOpenAI(model="gpt-4o-mini")
messages = [
    SystemMessage(content=f"You are a helpful assistant.\n\n{context_string}"),
    HumanMessage(content=user_query)
]
response = llm.invoke(messages)

# 4. Submit feedback in the background (Non-blocking)
ace.submit_feedback(
    interaction_id=interaction_id,
    user_feedback="The agent correctly validated the order first.",
    rating=5,
    model_response=response.content
)
```

### Azure OpenAI Support

ACE supports Azure OpenAI for its internal Reflector logic. Simply use the `azure_openai:` prefix and pass explicit credentials via `chat_model_kwargs`.

```python
ace = ACEClient(
    playbook_name="azure_deployment",
    chat_model="azure_openai:gpt-5-mini", # Deployment name
    chat_model_kwargs={
        "azure_endpoint": "https://your-resource.azure.com/",
        "api_key": "your-key",
        "api_version": "2024-10-01-preview"
    }
)
```

---

##  Architecture

```
┌─────────────────┐
│   Your App      │ ← Full control over LLM & Prompts
│   (Any Client)  │
└─────────┬───────┘
          │ (1) get_context(query)
          ▼
┌─────────────────┐
│   ACEClient     │ ← Dynamic context retrieval (Sync/Async)
│  (Provider)     │
└─────────┬───────┘
          │ (2) submit_feedback()
          ▼
┌─────────────────┐
│   Reflector     │ ← Background Analysis (Azure/OpenAI)
│   + Curator     │ ← Playbook Optimization
└─────────────────┘
```

### Components

| Component | Purpose | Uses LLM? | Key Features |
|-----------|---------|-----------|-------------|
| **ACEClient** | Central API for context & feedback | No | Non-blocking, Sync/Async support |
| **PlaybookManager** | Stores & retrieves knowledge | No | Semantic search via FAISS/Chroma/Qdrant |
| **Reflector** | Analyzes feedback, extracts insights |  Yes | Multi-iteration refinement, Azure support |
| **Curator** | Updates playbook deterministically |  No | Score-based rule optimization |
| **ACEAgent** | *Legacy* wrapper (Deprecated) | No | Maintained for backward compatibility |

---

##  Configuration

```python
from ace import ACEConfig

config = ACEConfig(
    playbook_name="my_app",
    chat_model="azure_openai:gpt-4o-mini", # For internal Reflector
    chat_model_kwargs={"api_key": "..."},   # Direct LangChain kwargs
    embedding_model="openai:text-embedding-3-small", 
    top_k=5 
)
```
# Note: Curator does NOT use LLM - it's deterministic.
# It uses embeddings via PlaybookManager for similarity matching.

### Storage Location

**FAISS/ChromaDB (Local Storage):**
By default, ACE stores playbooks in `./.ace/playbooks/{playbook_name}/` (like `.venv`):

```
your-project/
 .venv/              ← Virtual environment
 .ace/               ← ACE storage
    playbooks/
        my_app/
            faiss_index.bin  (or chromadb/)
            metadata.json
            playbook.md
 your_code.py
```

**Qdrant (External Vector Storage):**
With Qdrant, playbook metadata stays local, but vectors are stored externally:

```
your-project/
 .ace/
    playbooks/
        my_app/
            metadata.json      ← Local (bullet content, counters)
            playbook.md        ← Local
            # NO vector files   ← Vectors stored in Qdrant server

Qdrant Server (Docker/Cloud):
    Collection: my_app
        └── Vectors (embeddings) ← External
```

**Qdrant Setup:**
- **Local (Docker):** `docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant`
- **Cloud:** Get URL and API key from [Qdrant Cloud](https://cloud.qdrant.io/)

---

##  Examples

Check the [`examples/`](./examples/) directory for complete examples:
- **[basic_usage.py](./examples/basic_usage.py)** - Wrap an agent with ACE (start here!)
- **[with_feedback.py](./examples/with_feedback.py)** - Complete learning cycle
- **[chromadb_usage.py](./examples/chromadb_usage.py)** - Using ChromaDB vector store
- **[qdrant_usage.py](./examples/qdrant_usage.py)** - Using Qdrant (local Docker or Cloud)

---

##  Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run simple learning test (5 questions with feedback)
uv run pytest tests/test_simple_learning.py -v -s

# Or run directly (requires OPENAI_API_KEY in .env)
uv run python tests/test_simple_learning.py

# Run specific test suite
uv run pytest tests/test_e2e_learning.py -v -s

# Run with coverage
uv run pytest tests/ --cov=ace --cov-report=html
```

**All tests passing** ✓ 

---

##  Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

##  Documentation

- **[Technical Documentation](./docs/)** - Implementation details
- **[Paper Alignment](./docs/ACE_PAPER_ALIGNMENT.md)** - Research paper verification
- **[Implementation Summary](./docs/IMPLEMENTATION_SUMMARY.md)** - Complete technical summary

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

##  Acknowledgments

- **Research Paper:** [Agentic Context Engineering](http://arxiv.org/pdf/2510.04618) by Zhang et al. (Stanford/SambaNova, 2025)
- **Built with:** [LangChain](https://python.langchain.com/), [FAISS](https://github.com/facebookresearch/faiss), [ChromaDB](https://www.trychroma.com/), [Qdrant](https://qdrant.tech/)

---

##  Contact

- **Author:** Prashant Malge
- **Email:** prashantmalge101@gmail.com
- **GitHub:** [@SuyodhanJ6](https://github.com/SuyodhanJ6)
- **Issues:** [GitHub Issues](https://github.com/SuyodhanJ6/ace-context-engineering/issues)

---

<p align="center">
  <strong> Star this repo if you find it useful!</strong>
</p>
