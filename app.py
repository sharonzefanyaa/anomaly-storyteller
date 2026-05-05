import pytz
import numpy as np
import requests

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime


# INIT
app = Flask(__name__)
CORS(app)

N8N_WEBHOOK_URL = "https://sharzefa.app.n8n.cloud/webhook/ads-data-trigger"


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
            "morning" if 6 <= now.hour < 12 else
            "afternoon" if 12 <= now.hour < 18 else
            "evening" if 18 <= now.hour < 24 else
            "night"
        )
    }


# AUTO GENERATOR
def generate_auto_data():

    ctx = get_time_context()

    impressions = int(np.random.randint(3000, 50000))

    ctr = float(np.random.uniform(0.005, 0.12))
    clicks = int(impressions * ctr)

    conversion_rate = float(np.random.uniform(0.05, 0.50))
    registrations = int(clicks * conversion_rate)

    cost = int(clicks * np.random.randint(1000, 10000))

    cpc = int(cost / clicks) if clicks > 0 else 0
    cpa = int(cost / registrations) if registrations > 0 else 0

    frequency = float(round(np.random.uniform(1.0, 8.0), 2))

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
@app.route("/submit", methods=["POST"])
def submit():

    input_data = request.json

    payload = {
        **get_time_context(),
        **input_data,
        "source": "manual"
    }

    trigger_n8n(payload)

    return jsonify({
        "status": "sent_to_n8n",
        "data": payload
    })


# AUTO ENDPOINT
@app.route("/auto", methods=["POST"])
def auto_generate():

    data = generate_auto_data()

    trigger_n8n(data)

    return jsonify({
        "status": "success",
        "data": data
    })


# RUN
if __name__ == "__main__":
    app.run(debug=True)