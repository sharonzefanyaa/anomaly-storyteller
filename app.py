import pytz
import numpy as np
import requests
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime


# INIT
app = Flask(__name__)
CORS(app)

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")


# HELPERS
def trigger_n8n(data):
    try:
        print("🚀 Sending to n8n:", data)

        res = requests.post(
            N8N_WEBHOOK_URL,
            json=data,
            timeout=5
        )

        print("n8n status:", res.status_code)
        print("n8n response:", res.text)

    except Exception as e:
        print("❌ n8n error:", str(e))


# TIME CONTEXT
def get_time_context():
    tz = pytz.timezone("Asia/Jakarta")
    now = datetime.now(tz)

    return {
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "day_name": now.strftime("%A"),
        "is_weekend": 1 if now.weekday() >= 5 else 0,
        "time_of_day": (
            "morning" if 5 <= now.hour < 11 else
            "afternoon" if 11 <= now.hour < 17 else
            "evening" if 17 <= now.hour < 21 else
            "night" if 21 <= now.hour < 24 else
            "late night"
        )
    }


# AUTO GENERATOR
def generate_auto_data():

    ctx = get_time_context()

    impressions = int(np.random.randint(3000, 50000))
    clicks = int(impressions * np.random.uniform(0.01, 0.08))
    registrations = int(clicks * np.random.uniform(0.05, 0.40))
    cost = int(clicks * np.random.randint(1000, 10000))
    frequency = round(float(np.random.uniform(1.0, 8.0)), 2)

    return {
        **ctx,

        "platform": np.random.choice(["TikTok", "Instagram", "Facebook"]),
        "campaign_name": np.random.choice(["App Install", "Brand Awareness", "Retargeting"]),
        "campaign_status": np.random.choice(["ON", "PAUSED"]),
        "creative_type": np.random.choice(["video", "image", "carousel", "reels", "story"]),
        "audience_type": np.random.choice(["broad", "retargeting", "look alike", "custom audience"]),

        "impressions": impressions,
        "clicks": clicks,
        "registrations": registrations,
        "cost": cost,
        "frequency": frequency,

        "source": "auto"
    }


# MANUAL ENDPOINT
@app.route("/manual", methods=["POST"])
def manual_generate():

    input_data = request.json

    data = {
        **get_time_context(),
        **input_data,
        "source": "manual"
    }

    return jsonify({
        "status": "generated",
        "data": data
    })


# AUTO ENDPOINT
@app.route("/auto", methods=["POST"])
def auto_generate():

    data = generate_auto_data()

    return jsonify({
        "status": "generated",
        "data": data
    })

# SEND TO N8N ENDPOINT
@app.route("/send", methods=["POST"])
def send_to_n8n():

    data = request.json

    trigger_n8n(data)

    return jsonify({
        "status": "sent_to_n8n",
        "data": data
    })

# RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
