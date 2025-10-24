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

```bash
# Default (FAISS vector store)
pip install ace-context-engineering

# With ChromaDB support
pip install ace-context-engineering[chromadb]
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

```python
from ace import Reflector, Curator

# Initialize learning components
reflector = Reflector(
    model=config.chat_model,
    storage_path=config.get_storage_path()
)

curator = Curator(
    playbook_manager=playbook,
    storage_path=config.get_storage_path()
)

# Provide feedback
feedback = {
    "rating": "positive",
    "comment": "Payment processed successfully"
}

# Analyze and learn
insight = reflector.analyze_feedback(chat_data, feedback)
delta = curator.process_insights(insight, feedback_id)
curator.merge_delta(delta)

# Playbook automatically improves!
```

---

##  Architecture

```

  Your Agent       ← Any LangChain agent
  (Generator)    

         
    
     ACEAgent  ← Automatic context injection
     Wrapper 
    
         
    
      Playbook     ← Semantic knowledge retrieval
      Manager    
    
         
    
    Reflector      ← Analyzes feedback
    + Curator      ← Updates playbook
    
```

### Components

| Component | Purpose | Uses LLM? |
|-----------|---------|-----------|
| **ACEAgent** | Wraps your agent, injects context | No |
| **PlaybookManager** | Stores & retrieves knowledge | No (embeddings only) |
| **Reflector** | Analyzes feedback, extracts insights |  Yes |
| **Curator** | Updates playbook deterministically |  No |

---

##  Configuration

```python
from ace import ACEConfig

config = ACEConfig(
    playbook_name="my_app",           # Unique name for your app
    vector_store="faiss",             # or "chromadb"
    storage_path="./.ace/playbooks",  # Default: current directory
    chat_model="openai:gpt-4o-mini",  # Any LangChain model
    embedding_model="openai:text-embedding-3-small",
    temperature=0.3,
    top_k=10,                         # Number of bullets to retrieve
    deduplication_threshold=0.9       # Similarity threshold
)
```

### Storage Location

By default, ACE stores playbooks in `./.ace/playbooks/{playbook_name}/` (like `.venv`):

```
your-project/
 .venv/              ← Virtual environment
 .ace/               ← ACE storage
    playbooks/
        my_app/
            faiss_index.bin
            metadata.json
            playbook.md
 your_code.py
```

---

##  Examples

Check the [`examples/`](./examples/) directory for complete examples:

- **[agent_with_create_agent.py](./examples/agent_with_create_agent.py)** - Using create_agent (LangChain 1.0) 
- **[basic_usage.py](./examples/basic_usage.py)** - Wrap an agent with ACE (start here!)
- **[with_feedback.py](./examples/with_feedback.py)** - Complete learning cycle
- **[chromadb_usage.py](./examples/chromadb_usage.py)** - Using ChromaDB backend
- **[custom_prompts.py](./examples/custom_prompts.py)** - Customize Reflector prompts
- **[custom_top_k.py](./examples/custom_top_k.py)** - Configure top_k retrieval
- **[env_setup.py](./examples/env_setup.py)** - Environment configuration
- **[manual_control.py](./examples/manual_control.py)** - Fine-grained control

---

##  Use Cases

### 1. Customer Support Agents
Learn optimal response patterns from customer feedback.

### 2. Code Generation
Accumulate best practices and common patterns.

### 3. Data Analysis
Build domain-specific analysis strategies.

### 4. Task Automation
Improve workflows based on execution results.

---

##  Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test suite
uv run pytest tests/test_e2e_learning.py -v -s

# Run with coverage
uv run pytest tests/ --cov=ace --cov-report=html
```

**All 31 tests passing** 

---

##  Performance

From the research paper (Stanford/SambaNova, 2025):

| Metric | Improvement |
|--------|-------------|
| Task Performance | **+17.0%** |
| Domain Adaptation | **+12.8%** |
| Adaptation Speed | **82.3% faster** |
| Computational Cost | **75.1% lower** |

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
- **Built with:** [LangChain](https://python.langchain.com/), [FAISS](https://github.com/facebookresearch/faiss), [ChromaDB](https://www.trychroma.com/)

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
