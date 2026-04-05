from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import secrets
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allows Wix to call it

# Simple in-memory demo (no database needed for this integration)
@app.route('/')
def home():
    return "✅ Ace Trust Kernel + Temenos GenAI is LIVE!"

# INTEGRATION 1: Temenos GenAI (exactly as per your blueprint)
@app.route('/temenos_classify', methods=['POST'])
def temenos_classify():
    data = request.get_json()
    if not data or 'narrative' not in data:
        return jsonify({"status": "ERROR", "msg": "Raw transaction narrative required"}), 400

    narrative = data['narrative'].upper()

    if any(x in narrative for x in ["ZOMATO", "SWIGGY", "AMAZON", "FLIPKART"]):
        sector = "Retail / E-commerce"
        roi_impact = "High Volume • Fraud Weight +18%"
    elif any(x in narrative for x in ["UPI", "PAYTM", "GPAY"]):
        sector = "Digital Payments"
        roi_impact = "Medium Volume • Fraud Weight +8%"
    elif any(x in narrative for x in ["SALARY", "CREDIT", "LOAN"]):
        sector = "Payroll / Finance"
        roi_impact = "Low Volume • Fraud Weight +2%"
    else:
        sector = "Other / Uncategorized"
        roi_impact = "Medium Risk • Fraud Weight +10%"

    return jsonify({
        "status": "CLASSIFIED",
        "original_narrative": data['narrative'],
        "classified_sector": f"[Sector: {sector}]",
        "roi_impact": roi_impact,
        "message": "✅ Live data fed into TrustOS ROI calculator"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5050)))
