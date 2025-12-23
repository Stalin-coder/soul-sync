
import os
import requests
from flask import Flask, render_template_string, jsonify,request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TAVUS_API_KEY = ""
REPLICA_ID = "r6ae5b6efc9d"
API = "https://tavusapi.com/v2"
HEADERS = {"x-api-key": TAVUS_API_KEY, "Content-Type": "application/json"}


# 🔹 Built-in context (hard-coded persona / role)
# DEFAULT_CONTEXT = "You are a friendly AI tutor. Explain concepts clearly and step by step."

DEFAULT_CONTEXT = "You are Sara, a 28-year-old history teacher who specializes in US history. You have a calm, personable, and friendly demeanor. You're passionate about making history engaging and relevant to today's world. Your teaching style is conversational and interactive rather than lecture-based. You excel at asking thought-provoking questions that encourage critical thinking. When speaking with students, you maintain a warm and approachable tone while still being professional. You're enthusiastic about history but never condescending. You explain complex historical events in accessible ways, often drawing parallels to current events or using relatable analogies. You have a knack for storytelling and bringing historical figures to life through compelling narratives. You believe history is about people and their experiences, not just dates and facts. You encourage students to see multiple perspectives on historical events. Your responses will be spoken out loud, so avoid any formatting, bullet points, or stage directions. Speak naturally as you would in a one-on-one conversation. Don't refer to yourself as an AI, LLM, assistant, or any similar terms - you are simply Emma, a history teacher. You initiate conversations with a friendly greeting, then follow the student's lead. If they seem disengaged, you might try a different approach or ask what historical topics interest them most. Your goal is to make history interesting and accessible to everyone."

# HTML template (fullscreen avatar, no form)
HTML = """
<!doctype html>
<html>
<head>
  <title>Live AI Tutor</title>
  <style>
    body { margin: 0; padding: 0; }
    iframe {
      position: fixed;
      top: 0; left: 0;
      width: 100%;
      height: 100%;
      border: none;
      border-radius: 0;
      margin: 0;
      z-index: 9999;
    }
  </style>
</head>
<body>
  <iframe id="tavus-frame" allow="microphone; autoplay; clipboard-read; clipboard-write"
          src="{{ conversation_url }}"></iframe>

  <script>
    // End conversation when page closes
    window.addEventListener("beforeunload", function () {
      navigator.sendBeacon("/end_conversation", JSON.stringify({
        conversation_id: "{{ conversation_id }}"
      }));
    });
  </script>
</body>
</html>
"""

app = Flask(__name__)

# 🔹 Cleanup all active conversations (avoids 400 error)
def cleanup_all_conversations():
    try:
        r = requests.get(f"{API}/conversations", headers=HEADERS, timeout=30)
        if r.ok:
            data = r.json().get("data", [])
            for conv in data:
                cid = conv.get("conversation_id")
                if cid:
                    requests.delete(f"{API}/conversations/{cid}", headers=HEADERS, timeout=30)
    except Exception as e:
        print("Cleanup failed:", e)


@app.route("/", methods=["GET"])
def index():
    # Cleanup old sessions first
    cleanup_all_conversations()

    # Create a new conversation with built-in context
    body = {"replica_id": REPLICA_ID, "conversational_context": DEFAULT_CONTEXT}
    r = requests.post(f"{API}/conversations", headers=HEADERS, json=body, timeout=60)

    if not r.ok:
        return f"<h2>Error {r.status_code}</h2><pre>{r.text}</pre>", r.status_code

    data = r.json()
    conversation_url = data.get("conversation_url")
    conversation_id = data.get("conversation_id")

    return render_template_string(HTML, conversation_url=conversation_url, conversation_id=conversation_id)


@app.route("/end_conversation", methods=["POST"])
def end_conversation():
    data = request.get_json()
    conversation_id = data.get("conversation_id")
    if conversation_id:
        url = f"{API}/conversations/{conversation_id}"
        r = requests.delete(url, headers=HEADERS, timeout=30)
        if not r.ok:
            return jsonify({"status": "error", "message": r.text}), r.status_code
        return jsonify({"status": "ok", "message": "Conversation ended"})
    return jsonify({"status": "error", "message": "No conversation_id provided"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5002)


# import os
# import requests
# from flask import Flask, render_template_string, jsonify, request
# from dotenv import load_dotenv
# from openai import OpenAI

# # Load env variables
# load_dotenv()
# # TAVUS_API_KEY = os.getenv("TAVUS_API_KEY", "your_tavus_api_key")
# # REPLICA_ID = os.getenv("TAVUS_REPLICA_ID", "your_replica_id_here")
# # OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your_openrouter_key")
# TAVUS_API_KEY = ""
# REPLICA_ID = "r6ae5b6efc9d"
# OPENROUTER_API_KEY = "sk-or"

# # Tavus setup
# API = "https://tavusapi.com/v2"
# HEADERS = {"x-api-key": TAVUS_API_KEY, "Content-Type": "application/json"}

# # OpenRouter client
# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=OPENROUTER_API_KEY,
# )

# # Hardcoded persona/context
# DEFAULT_CONTEXT = "You are a friendly AI tutor. Explain concepts clearly and step by step."

# # HTML: fullscreen iframe, mic only
# HTML = """
# <!doctype html>
# <html>
# <head>
#   <title>AI Tutor</title>
#   <style>
#     body { margin: 0; padding: 0; }
#     iframe {
#       position: fixed;
#       top: 0; left: 0;
#       width: 100%;
#       height: 100%;
#       border: none;
#       border-radius: 0;
#       margin: 0;
#       z-index: 9999;
#     }
#   </style>
# </head>
# <body>
#   <iframe id="tavus-frame" allow="microphone; autoplay; clipboard-read; clipboard-write"
#           src="{{ conversation_url }}"></iframe>

#   <script>
#     // End conversation when page closes
#     window.addEventListener("beforeunload", function () {
#       navigator.sendBeacon("/end_conversation", JSON.stringify({
#         conversation_id: "{{ conversation_id }}"
#       }));
#     });
#   </script>
# </body>
# </html>
# """

# app = Flask(__name__)

# # ---------- Tavus Utils ----------
# def cleanup_all_conversations():
#     """Delete all active Tavus conversations to avoid 'max concurrent' error"""
#     try:
#         r = requests.get(f"{API}/conversations", headers=HEADERS, timeout=30)
#         if r.ok:
#             data = r.json().get("data", [])
#             for conv in data:
#                 cid = conv.get("conversation_id")
#                 if cid:
#                     requests.delete(f"{API}/conversations/{cid}", headers=HEADERS, timeout=30)
#     except Exception as e:
#         print("Cleanup failed:", e)


# def send_to_tavus(conversation_id, text):
#     """Send a new message to the Tavus avatar to speak"""
#     url = f"{API}/conversations/{conversation_id}/messages"
#     body = {"role": "assistant", "content": text}
#     r = requests.post(url, headers=HEADERS, json=body, timeout=30)
#     if not r.ok:
#         print("Tavus message error:", r.text)
#     return r.ok


# # ---------- OpenRouter Utils ----------
# def get_ai_response(user_message):
#     """Ask OpenRouter (DeepSeek model) and return text"""
#     completion = client.chat.completions.create(
#         extra_headers={
#             "HTTP-Referer": "http://localhost:5002",  # optional
#             "X-Title": "AI Tutor Demo",               # optional
#         },
#         model="deepseek/deepseek-chat-v3.1:free",
#         messages=[
#             {"role": "system", "content": DEFAULT_CONTEXT},
#             {"role": "user", "content": user_message}
#         ]
#     )
#     return completion.choices[0].message.content


# # ---------- Routes ----------
# @app.route("/", methods=["GET"])
# def index():
#     # cleanup old sessions
#     cleanup_all_conversations()

#     # create new Tavus conversation
#     body = {"replica_id": REPLICA_ID, "conversational_context": DEFAULT_CONTEXT}
#     r = requests.post(f"{API}/conversations", headers=HEADERS, json=body, timeout=60)

#     if not r.ok:
#         return f"<h2>Error {r.status_code}</h2><pre>{r.text}</pre>", r.status_code

#     data = r.json()
#     conversation_url = data.get("conversation_url")
#     conversation_id = data.get("conversation_id")

#     return render_template_string(HTML, conversation_url=conversation_url, conversation_id=conversation_id)


# @app.route("/chat", methods=["POST"])
# def chat():
#     """User message → OpenRouter → Tavus avatar speaks"""
#     data = request.get_json()
#     user_message = data.get("message", "")
#     conversation_id = data.get("conversation_id")

#     if not user_message or not conversation_id:
#         return jsonify({"error": "message and conversation_id required"}), 400

#     # 1. Get response from OpenRouter
#     ai_reply = get_ai_response(user_message)

#     # 2. Send reply to Tavus for avatar to speak
#     send_ok = send_to_tavus(conversation_id, ai_reply)

#     return jsonify({"reply": ai_reply, "sent_to_tavus": send_ok})


# @app.route("/end_conversation", methods=["POST"])
# def end_conversation():
#     data = request.get_json()
#     conversation_id = data.get("conversation_id")
#     if conversation_id:
#         url = f"{API}/conversations/{conversation_id}"
#         r = requests.delete(url, headers=HEADERS, timeout=30)
#         if not r.ok:
#             return jsonify({"status": "error", "message": r.text}), r.status_code
#         return jsonify({"status": "ok", "message": "Conversation ended"})
#     return jsonify({"status": "error", "message": "No conversation_id provided"}), 400


# if __name__ == "__main__":
#     app.run(debug=True, port=5002)
# TAVUS_API_KEY = ""
