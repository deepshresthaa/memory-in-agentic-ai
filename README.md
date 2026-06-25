# Mem0 Interview Prep Agent

This project demonstrates how to build a lightweight interview-prep assistant that remembers prior interactions and uses that memory to personalize follow-up questions.

## Why memory matters

Large language models are naturally stateless. Without memory, each conversation starts fresh and the assistant cannot remember what the user said earlier, which makes follow-up questions repetitive and less helpful.

Mem0 solves this by giving the application a persistent memory layer. Instead of treating every prompt as a brand-new interaction, the app can retrieve relevant past context, such as prior answers, weak areas, and career goals, and use that information to make better decisions.

## The Mem0 directory

The project uses a local `.mem0` directory as the default storage location for Mem0-related state. In the code, the environment variable `MEM0_DIR` is set to the project’s `.mem0` folder so the app has a predictable place to keep local memory data.

You can think of this directory as the local workspace for Mem0’s runtime state while the vector store is backed by Qdrant in the `qdrant_data` folder.

## Project initialization

Follow these steps to initialize and run the project locally.

1. Create and activate a Python virtual environment.

   On Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the required API keys and environment values. For example:

   ```env
   GROQ_API_KEY=your_groq_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

   The app also uses a local `.mem0` folder automatically, so you do not need to create it manually.

4. Run a quick smoke test from Python.

   ```bash
   python
   ```

   Then inside the Python shell:

   ```python
   from memory_agent import chat

   print(chat("demo-user", "Help me prepare for a software engineering interview"))
   ```

   This will initialize Mem0, search for prior memory, and generate a response.

## Architecture flow

A simple view of the request flow looks like this:

```text
User message
  -> Streamlit UI
  -> memory_agent.py
  -> Mem0
  -> Qdrant vector store
  -> Mem0
  -> memory_agent.py
  -> LangChain
  -> Groq model
  -> LangChain
  -> Streamlit UI
```

In practice, the app uses Mem0 to retrieve relevant prior memories, passes that context into the prompt, and then sends the enriched request to the Groq-backed language model for a response.

## Notes

- The project currently uses a local Qdrant store under `qdrant_data` for vector search.
- The chat logic lives in `memory_agent.py`.
- The `.mem0` folder is used for Mem0’s local runtime state and memory artifacts.
