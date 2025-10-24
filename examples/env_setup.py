"""
Environment Setup Example for ACE.

Shows different ways to load API keys and environment variables.
"""

print(" ACE Environment Setup Examples\n")

# Method 1: Auto-load (happens automatically on import)
print("=" * 60)
print("Method 1: Auto-load .env (Default Behavior)")
print("=" * 60)
print("""
When you import ace, it automatically tries to load .env file:

    from ace import ACEConfig  # .env loaded automatically!
    
The .env file is searched in:
1. Current directory
2. Parent directories (up to root)
""")

# Method 2: Explicit load
print("\n" + "=" * 60)
print("Method 2: Explicit load_env()")
print("=" * 60)

from ace.utils import load_env

# Load .env file
loaded = load_env(verbose=True)

if loaded:
    print(" Environment variables loaded from .env file")
else:
    print("ℹ  No .env file found (using system environment)")

# Method 3: Check API keys
print("\n" + "=" * 60)
print("Method 3: Check which API keys are set")
print("=" * 60)

from ace.utils import check_api_keys

# Check common API keys
check_api_keys(["openai", "anthropic"], verbose=True)

# Method 4: Get specific API key
print("\n" + "=" * 60)
print("Method 4: Get specific API key")
print("=" * 60)

from ace.utils import get_api_key

openai_key = get_api_key("openai")
if openai_key:
    # Mask the key for security
    masked = openai_key[:8] + "..." + openai_key[-4:]
    print(f" OpenAI API Key: {masked}")
else:
    print(" OpenAI API Key not set")

# Method 5: Ensure API key (raises error if not set)
print("\n" + "=" * 60)
print("Method 5: Ensure API key is set")
print("=" * 60)

from ace.utils import ensure_api_key

try:
    key = ensure_api_key("openai")
    print(" OpenAI API key verified")
except ValueError as e:
    print(f" Error: {e}")

# Method 6: Custom .env file path
print("\n" + "=" * 60)
print("Method 6: Load from custom path")
print("=" * 60)
print("""
You can specify a custom .env file:

    from ace.utils import load_env
    load_env("/path/to/custom/.env")
""")

# Method 7: Disable auto-load
print("\n" + "=" * 60)
print("Method 7: Disable auto-load")
print("=" * 60)
print("""
To disable automatic .env loading:

    export ACE_AUTO_LOAD_ENV=false
    
Or in your .env file:
    
    ACE_AUTO_LOAD_ENV=false
""")

# Summary
print("\n" + "=" * 60)
print(" Quick Setup Guide")
print("=" * 60)
print("""
1. Copy .env.example to .env:
   cp .env.example .env

2. Edit .env and add your API keys:
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...

3. Use ACE normally - environment loads automatically:
   from ace import ACEConfig, PlaybookManager
   config = ACEConfig()
   playbook = PlaybookManager(...)

4. Or explicitly load:
   from ace.utils import load_env
   load_env(verbose=True)
""")

print("\n Environment setup guide complete!")

