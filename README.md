# ACE Context Engineering

[![PyPI version](https://badge.fury.io/py/ace-context-engineering.svg)](https://badge.fury.io/py/ace-context-engineering)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Self-improving AI agents through evolving playbooks.** Wrap any LangChain agent with ACE to enable learning from experience without fine-tuning.

 **Based on research:** [Agentic Context Engineering (Stanford/SambaNova, 2025)](http://arxiv.org/pdf/2510.04618)

---

##  What is ACE?

ACE enables AI agents to **learn and improve** by accumulating strategies in a "playbook" - a knowledge base that grows smarter with each interaction.

### Key Benefits

-  **+17% task performance** improvement
-  **82% faster** adaptation to new domains  
-  **75% lower** computational cost vs fine-tuning
-  **Zero model changes** - works with any LLM

---

##  Installation

### Using pip
```bash
# Default (FAISS vector store)
pip install ace-context-engineering

# With ChromaDB support
pip install ace-context-engineering[chromadb]

# With Qdrant support
pip install ace-context-engineering[qdrant]
# or: pip install qdrant-client
```

### Using uv (Recommended)
```bash
# Default (FAISS vector store)
uv add ace-context-engineering

# With ChromaDB support
uv add ace-context-engineering[chromadb]

# With Qdrant support
uv add ace-context-engineering[qdrant]
# or: uv add qdrant-client
```

**Environment Setup:**

```bash
# Copy example environment file
cp .env.example .env

# Add your API key
echo "OPENAI_API_KEY=your-key-here" >> .env
```

---

##  Quick Start

### 3-Step Integration

```python
from ace import ACEConfig, ACEAgent, PlaybookManager
from langchain.chat_models import init_chat_model

# 1. Configure ACE
config = ACEConfig(
    playbook_name="my_app",
    vector_store="faiss",
    top_k=10
)

playbook = PlaybookManager(
    playbook_dir=config.get_storage_path(),
    vector_store=config.vector_store,
    embedding_model=config.embedding_model
)

# 2. Wrap your agent
base_agent = init_chat_model("openai:gpt-4o-mini")
agent = ACEAgent(
    base_agent,
    playbook,
    config,
    auto_inject=True  # Automatic context injection
)

# 3. Use normally - ACE handles context automatically!
response = agent.invoke([
    {"role": "user", "content": "Process payment for order #12345"}
])

# 4. Provide feedback for learning (optional but recommended)
chat_data = agent.get_last_interaction()  # Get interaction data
result = agent.submit_feedback(
    user_feedback="Payment processed successfully",
    rating=5,
    chat_data=chat_data  # Explicit for production/parallel users
)
```

### Add Knowledge to Playbook

```python
# Add strategies manually
playbook.add_bullet(
    content="Always validate order exists before processing payment",
    section="Payment Processing"
)

playbook.add_bullet(
    content="Log all failed transactions with error codes",
    section="Error Handling"
)
```

### Learning from Feedback

**Simple API (Recommended):**

```python
# After agent response, provide feedback
chat_data = agent.get_last_interaction()  # Get current interaction data

result = agent.submit_feedback(
    user_feedback="Payment processed successfully",
    rating=5,  # 1-5 scale
    feedback_type="positive",
    chat_data=chat_data  # Explicit for thread-safety in production
)

# ACE automatically:
# 1. Reflector analyzes feedback → extracts insights
# 2. Curator creates/updates playbook bullets
# 3. Playbook improves for future interactions!
```

**For Async/Parallel Users:**

```python
# Use async API for better performance
chat_data = {
    "question": user_question,
    "model_response": response.content,
    "used_bullets": agent.get_used_bullets()
}

result = await agent.asubmit_feedback(
    user_feedback="Great response!",
    rating=5,
    chat_data=chat_data  # Required for thread-safety
)
```

---

##  Architecture

```
┌─────────────────┐
│   Your Agent    │ ← Any LangChain agent
│   (Generator)   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   ACEAgent      │ ← Automatic context injection
│   Wrapper       │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   Playbook      │ ← Semantic knowledge retrieval
│   Manager       │
└─────────────────┘
          ▲
          │
┌─────────────────┐
│   Reflector     │ ← Analyzes feedback
│   + Curator     │ ← Updates playbook
└─────────────────┘
```

### Components

| Component | Purpose | Uses LLM? | Key Features |
|-----------|---------|-----------|-------------|
| **ACEAgent** | Wraps your agent, injects context | No | Thread-safe with `chat_data` param, async support |
| **PlaybookManager** | Stores & retrieves knowledge | No | Uses embeddings for semantic search |
| **Reflector** | Analyzes feedback, extracts insights |  Yes | Multi-iteration refinement, auto-critique |
| **Curator** | Updates playbook deterministically |  No | Uses embeddings for similarity matching (no LLM) |

---

##  Configuration

```python
from ace import ACEConfig

config = ACEConfig(
    playbook_name="my_app",           # Unique name for your app
    vector_store="faiss",             # "faiss", "chromadb", "qdrant", or "qdrant-cloud"
    storage_path="./.ace/playbooks",  # Optional: custom path
    chat_model="openai:gpt-4o-mini",  # For Reflector (feedback analysis)
    embedding_model="openai:text-embedding-3-small",  # For semantic search
    temperature=0.3,                  # LLM temperature
    top_k=10,                         # Number of bullets to retrieve
    deduplication_threshold=0.9,      # Similarity threshold for deduplication
    # Qdrant-specific (only needed for qdrant/qdrant-cloud)
    qdrant_url="http://localhost:6333",  # Qdrant server URL
    qdrant_api_key=None               # Required for qdrant-cloud, optional for qdrant
)

# Note: Curator does NOT use LLM - it's deterministic
# Curator uses embeddings via PlaybookManager for similarity matching
```

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
