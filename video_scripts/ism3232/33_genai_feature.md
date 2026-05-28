# Video 33: Integrating a GenAI Feature (Anthropic API)

## YouTube Metadata

**Title:** Add a Controlled AI Feature to Your Streamlit App — Anthropic API | ISM3232
**Description:**
Add a production-grade AI feature to your capstone Streamlit app using the Anthropic API. This video covers the six required GenAI controls for ISM3232: system prompt, user confirmation, output preview, max tokens, rate limiting, and disclaimer — plus secure API key handling and a complete working implementation.

**Chapters:**
0:00 — What a "controlled" AI feature means
2:00 — Installing the Anthropic SDK
3:30 — Secure API key handling with .env
5:30 — Basic API call
8:00 — The six required controls
13:00 — Complete implementation in Streamlit
17:00 — Final repo checklist
19:30 — Presentation structure
21:30 — Recap

**Applies to:** ISM3232 Module 16

**Tags:** anthropic API, claude API, python AI, streamlit AI, genai feature, python anthropic, ISM3232, claude python, AI capstone project, controlled AI, responsible AI development

---

## Script

### INTRO (0:00–2:00)

The capstone's GenAI feature is not a chatbot. It's not an open-ended "ask AI anything" box. It's a **controlled** AI capability — a specific, bounded use of the Anthropic API that solves one well-defined business problem in your application.

"Controlled" means six things: a system prompt that defines scope, user confirmation before sending, output preview before saving, token limits, rate limiting, and a visible disclaimer. These aren't bureaucracy — they're the difference between a professional AI integration and a liability. Let's build it right.

---

### WHAT COUNTS AS A CONTROLLED FEATURE (0:00–2:00, continued)

Good examples:
- "Generate a reorder recommendation for products with low stock"
- "Summarize this customer's purchase history in one paragraph"
- "Suggest a product description based on name and category"
- "Flag this expense report entry as unusual or routine"

Not good examples:
- "Chat with Claude about anything"
- "Let users write their own prompts"
- "Use AI to make financial decisions autonomously"

The AI feature should do one specific thing related to your business domain. The prompt is fixed. The user provides data, not instructions.

---

### INSTALLING ANTHROPIC SDK (2:00–3:30)

```bash
pip install anthropic python-dotenv
pip freeze > requirements.txt
```

Import:

```python
import anthropic
```

---

### API KEY HANDLING (3:30–5:30)

Your API key is a secret. Never hardcode it. Never commit it to GitHub.

Create a `.env` file in your project root:

```
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

Add `.env` to `.gitignore` immediately:

```
.env
```

Load it in Python with `python-dotenv`:

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()   # reads .env and sets environment variables

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    raise EnvironmentError("ANTHROPIC_API_KEY not set. Add it to .env file.")
```

In your app:

```python
import anthropic
from config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
```

Alternatively, if `ANTHROPIC_API_KEY` is set as an environment variable (which it will be from `.env` via `load_dotenv()`), the Anthropic client picks it up automatically:

```python
client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from environment
```

---

### BASIC API CALL (5:30–8:00)

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-haiku-4-5-20251001",   # fast, affordable, good for structured tasks
    max_tokens=256,
    system="You are a business inventory analyst. Respond in plain English. Be concise.",
    messages=[
        {"role": "user", "content": "The product 'Laptop Bag' has 2 units remaining. Should we reorder?"}
    ]
)

response_text = message.content[0].text
print(response_text)
```

Key parameters:
- `model` — which Claude model to use. Haiku is fastest/cheapest for simple tasks. Sonnet for more complex reasoning.
- `max_tokens` — maximum tokens in the response. Controls cost and length.
- `system` — system prompt, defines the AI's role and constraints
- `messages` — the conversation. For a single-turn feature, one user message.

---

### THE SIX REQUIRED CONTROLS (8:00–13:00)

**Control 1 — System Prompt.** Defines the AI's role, constraints, and output format. Never let users modify this.

```python
SYSTEM_PROMPT = """You are an inventory management assistant for a campus bookstore.
Your only job is to analyze product stock levels and provide brief reorder recommendations.
Format: one sentence recommendation, then bullet points with specific actions.
Never discuss topics unrelated to inventory management.
Never make financial commitments or purchase orders."""
```

**Control 2 — User Confirmation.** Show the user what will be sent before sending it.

```python
st.subheader("AI Reorder Recommendation")

product_context = f"""
Product: {selected_product['name']}
Category: {selected_product['category']}
Current stock: {selected_product['quantity']} units
Price: ${selected_product['price']:.2f}
"""

st.info("The following information will be sent to Claude:")
st.code(product_context)

if not st.button("Generate Recommendation"):
    st.stop()   # don't proceed until confirmed
```

**Control 3 — Output Preview Before Saving.** Show the AI output; let the user accept or discard. Don't auto-save AI-generated content.

```python
# After getting the response:
st.subheader("AI Recommendation")
st.write(response_text)

col1, col2 = st.columns(2)
with col1:
    if st.button("✅ Accept and Save to Notes"):
        # save to database
        pass
with col2:
    if st.button("❌ Discard"):
        st.rerun()
```

**Control 4 — Max Tokens.** Set a reasonable limit. For a one-paragraph recommendation, 256 is plenty. For a detailed analysis, 512. Never use 4096 for a simple feature.

```python
max_tokens=256
```

**Control 5 — Rate Limiting.** Prevent accidental API cost explosions. Use `st.session_state` to track call frequency.

```python
import time

if "last_ai_call" not in st.session_state:
    st.session_state.last_ai_call = 0

RATE_LIMIT_SECONDS = 10   # minimum seconds between AI calls

elapsed = time.time() - st.session_state.last_ai_call
if elapsed < RATE_LIMIT_SECONDS:
    wait = int(RATE_LIMIT_SECONDS - elapsed)
    st.warning(f"Please wait {wait}s before making another AI request.")
    st.stop()

# After the call:
st.session_state.last_ai_call = time.time()
```

**Control 6 — Visible Disclaimer.** AI output is not authoritative. Say so.

```python
st.caption(
    "⚠️ This recommendation is generated by AI and may not reflect current supplier "
    "pricing or availability. Always verify before placing orders."
)
```

---

### COMPLETE IMPLEMENTATION (13:00–17:00)

```python
# ai_feature.py — complete controlled GenAI feature

import anthropic
import streamlit as st
import time
from database import get_all_products
from pathlib import Path

DB = Path("capstone.db")

SYSTEM_PROMPT = """You are an inventory management assistant for a campus bookstore.
Analyze the product information provided and give a brief reorder recommendation.
Format your response as:
1. One-sentence summary (recommend reorder or not)
2. Reasoning (2-3 bullet points)
3. Suggested action (one clear next step)

Keep your total response under 150 words. Never discuss unrelated topics."""

RATE_LIMIT_SECONDS = 15
MAX_TOKENS = 256

def render_ai_feature():
    st.header("🤖 AI Reorder Advisor")
    st.caption(
        "⚠️ AI recommendations are informational only. Verify with supplier before ordering."
    )

    products = get_all_products(DB)
    if not products:
        st.info("Add products first.")
        return

    # Select product
    product_map = {f"{p['name']} (qty: {p['quantity']})": p for p in products}
    selected_label = st.selectbox("Select a product to analyze:", list(product_map.keys()))
    product = product_map[selected_label]

    # Build prompt
    prompt = (
        f"Product: {product['name']}\n"
        f"Category: {product['category']}\n"
        f"Current quantity: {product['quantity']} units\n"
        f"Unit price: ${product['price']:.2f}\n"
        f"Should we reorder this product?"
    )

    # Control 2: Show what will be sent
    with st.expander("📋 Data being sent to AI"):
        st.code(prompt)

    # Control 5: Rate limiting
    if "last_ai_call" not in st.session_state:
        st.session_state.last_ai_call = 0

    elapsed = time.time() - st.session_state.last_ai_call
    if elapsed < RATE_LIMIT_SECONDS:
        wait = int(RATE_LIMIT_SECONDS - elapsed)
        st.warning(f"Rate limit: wait {wait}s before next request.")
        generate_enabled = False
    else:
        generate_enabled = True

    # Control 2: Confirmation button
    if st.button("Generate Recommendation", disabled=not generate_enabled):
        with st.spinner("Consulting AI..."):
            try:
                client = anthropic.Anthropic()
                message = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=MAX_TOKENS,   # Control 4
                    system=SYSTEM_PROMPT,    # Control 1
                    messages=[{"role": "user", "content": prompt}]
                )
                response = message.content[0].text
                st.session_state.last_ai_call = time.time()   # Control 5
                st.session_state.ai_response = response
                st.session_state.ai_product  = product["name"]

            except anthropic.APIError as e:
                st.error(f"API error: {e}")
                return

    # Control 3: Show output and let user accept/discard
    if "ai_response" in st.session_state:
        st.subheader(f"Recommendation for: {st.session_state.ai_product}")
        st.write(st.session_state.ai_response)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Accepted — noted for review"):
                del st.session_state.ai_response
                st.success("Recommendation noted.")
        with col2:
            if st.button("❌ Discard"):
                del st.session_state.ai_response
                st.rerun()
```

Call from `app.py`:
```python
from ai_feature import render_ai_feature

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["View All", "Add", "Update", "Deactivate", "🤖 AI Advisor"]
)
with tab5:
    render_ai_feature()
```

---

### FINAL REPO CHECKLIST (17:00–19:30)

Before your final presentation:

```
□ app.py runs with streamlit run app.py — no errors
□ All 5 Streamlit features work
□ AI feature has all 6 controls implemented
□ .env is in .gitignore — NEVER committed
□ requirements.txt is up to date (pip freeze > requirements.txt)
□ README.md explains: what the app does, how to run it, how to set API key
□ All 5 database functions present in database.py
□ Tests pass: pytest -v
□ ruff check . — no lint errors
□ All code committed and pushed
□ GitHub URL accessible and shows all files
□ Canvas submission has correct GitHub URL
```

---

### PRESENTATION STRUCTURE (19:30–21:30)

Your 8-minute final presentation covers:
1. **Business problem** — what does this app solve? (1 min)
2. **Live demo** — show all 5 Streamlit features (3 min)
3. **AI feature demo** — run it live, explain the 6 controls (2 min)
4. **Technical stack** — Python, SQLite, Streamlit, Claude API (1 min)
5. **What you'd add next** — 2-3 features you'd build with more time (1 min)

Practice the demo at least 3 times before presenting. Know which product data to use, what inputs to enter, and what output to expect. Never demo live without a rehearsal.

---

### RECAP (21:30–22:30)

- Use a specific, bounded AI feature — not an open-ended chatbot
- **6 controls:** system prompt, user confirmation, output preview, max tokens, rate limit, disclaimer
- Store API key in `.env`, never in code, never on GitHub
- `anthropic.Anthropic()` reads `ANTHROPIC_API_KEY` from environment automatically
- `claude-haiku-4-5-20251001` — fast and cost-effective for simple structured tasks
- `st.session_state` for rate limiting and preserving AI output across re-runs
- Preview before saving — never auto-commit AI-generated content to the database
- Run the full submission ritual before final submission

Congratulations on completing ISM3232.
