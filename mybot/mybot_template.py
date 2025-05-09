# mybot/mybot_template.py

import os
import replicate
import httpx
import logging
import traceback
from dotenv import load_dotenv

# — Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# — Load .env
load_dotenv()
API_TOKEN      = os.getenv("REPLICATE_API_TOKEN")
DEFAULT_MODEL  = os.getenv("REPLICATE_MODEL", "meta/meta-llama-3-70b")

if not API_TOKEN:
    raise ValueError("Set REPLICATE_API_TOKEN in your .env file")

# — Configure HTTPX timeout: 5 min read, no limit on connect/write/pool
timeout = httpx.Timeout(connect=None, read=300.0, write=None, pool=None)
client  = replicate.Client(api_token=API_TOKEN, timeout=timeout)


def process_message(history, user_input, model_id=None):
    """
    Streams chat responses from the specified Replicate model.
    :param history: List of {"role":…, "content":…} dicts
    :param user_input: String of the user's message
    :param model_id: Optional override of DEFAULT_MODEL
    :yields: (updated_history, thinking_slot, textbox_reset) tuples for Gradio
    """
    # 1️⃣ Choose model
    model_to_use = model_id or DEFAULT_MODEL

    # 2️⃣ Echo user message
    new_history = history + [{"role": "user", "content": user_input}]
    yield new_history, "", ""

    # 3️⃣ Build system + dynamic user prompt
    system_message = "You are a helpful, insightful AI assistant."
    prompt = f"{system_message}\n\n{user_input}"

    # 4️⃣ Prepare full params block
    params = {
        "prompt": prompt,
        "top_k": 0,
        "top_p": 0.9,
        "max_tokens": 512,
        "min_tokens": 0,
        "temperature": 0.6,
        "length_penalty": 1,
        "stop_sequences": "<|end_of_text|>",
        "prompt_template": "{prompt}",
        "presence_penalty": 1.15,
        "log_performance_metrics": False,
    }

    # 5️⃣ Invoke the model stream
    try:
        stream = client.stream(model_to_use, input=params)
    except Exception as e:
        logger.error("Stream invocation failed:\n" + traceback.format_exc())
        err = f"❌ Could not call `{model_to_use}`:\n{e}"
        yield new_history + [{"role": "assistant", "content": err}], "", ""
        return

    # 6️⃣ Stream chunks into the chat
    assistant_reply = ""
    for chunk in stream:
        assistant_reply += str(chunk)
        yield new_history + [{"role": "assistant", "content": assistant_reply}], "", ""

    # 7️⃣ Final message
    yield new_history + [{"role": "assistant", "content": assistant_reply}], "", ""
