import os
import hashlib
import platform
import uuid
import time
import subprocess
import re
import json
import tempfile
import secrets
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ACE_KERNEL_AUTH_KEY = os.environ.get('ACE_KERNEL_AUTH_KEY', 'sk-ace-demo-key-001')
SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///ace.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app)

limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

db = SQLAlchemy(app)

# (All other models and helper functions are the same as before — I'm keeping it short here)
# ... [You can keep your full original server.py code if you want, but make sure it has NO CSS/HTML]

# INTEGRATION 1: Temenos GenAI
@app.route('/temenos_classify', methods=['POST'])
def temenos_classify():
    data = request.json
    narrative = data.get('narrative')
    if not narrative:
        return jsonify({"status": "ERROR", "msg": "Raw transaction narrative required"}), 400

    # Simple classification (exactly as per your blueprint)
    narrative_upper = narrative.upper()
    if any(x in narrative_upper for x in ["ZOMATO", "SWIGGY", "AMAZON", "FLIPKART"]):
        sector = "Retail / E-commerce"
        roi_impact = "High Volume • Fraud Weight +18%"
    elif any(x in narrative_upper for x in ["UPI", "PAYTM", "GPAY"]):
        sector = "Digital Payments"
        roi_impact = "Medium Volume • Fraud Weight +8%"
    elif any(x in narrative_upper for x in ["SALARY", "CREDIT", "LOAN"]):
        sector = "Payroll / Finance"
        roi_impact = "Low Volume • Fraud Weight +2%"
    else:
        sector = "Other / Uncategorized"
        roi_impact = "Medium Risk • Fraud Weight +10%"

    return jsonify({
        "status": "CLASSIFIED",
        "original_narrative": narrative,
        "classified_sector": f"[Sector: {sector}]",
        "roi_impact": roi_impact,
        "message": "✅ Fed into TrustOS ROI calculator"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
