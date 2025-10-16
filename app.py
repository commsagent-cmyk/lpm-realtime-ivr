from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
  return "✅ LPM Realtime server is alive."

if __name__ == "__main__":
    # Render will set PORT for us later; this is fine for local.
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
