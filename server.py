<!DOCTYPE html>
<html>
<head>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    .trustos-container {
      max-width: 100%;
      margin: 0 auto;
      padding: 30px;
      background: linear-gradient(135deg, #0a0a2a, #1a1a3a);
      border-radius: 16px;
      color: #fff;
      font-family: 'Inter', sans-serif;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    .header { text-align: center; margin-bottom: 25px; }
    .header h2 { color: #00d4ff; font-size: 24px; margin: 0; }
    .header p { color: #aaa; font-size: 14px; }
    input[type="text"] {
      width: 100%;
      padding: 15px;
      border: none;
      border-radius: 8px;
      background: #fff;
      color: #000;
      font-size: 16px;
      margin-bottom: 15px;
    }
    button {
      background: #00d4ff;
      color: #000;
      border: none;
      padding: 14px 28px;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
      width: 100%;
      font-size: 16px;
    }
    button:hover { background: #00ffcc; }
    .result {
      display: none;
      background: rgba(255,255,255,0.1);
      border-radius: 12px;
      padding: 20px;
      margin-top: 20px;
    }
    .sector-tag {
      display: inline-block;
      background: #00ff88;
      color: #000;
      padding: 6px 16px;
      border-radius: 50px;
      font-weight: 600;
      font-size: 15px;
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <div class="trustos-container">
    <div class="header">
      <h2>🔗 TrustOS + Temenos GenAI</h2>
      <p>Live Transaction Classification (PQC-sealed)</p>
    </div>

    <input type="text" id="narrative" placeholder="e.g. ZOMATO-ORDER-123" value="ZOMATO-ORDER-123">

    <button onclick="classifyTransaction()">Classify with Temenos GenAI</button>

    <div id="result" class="result">
      <h3>✅ Temenos GenAI Result:</h3>
      <p id="classified-text" style="margin:10px 0; font-size:15px;"></p>
      <strong>Sector:</strong> <span id="sector-tag" class="sector-tag"></span><br><br>
      <strong>TrustOS ROI Impact:</strong> <span id="roi-impact" style="color:#00ff88; font-weight:600;"></span>
      <div style="margin-top:15px; font-size:12px; color:#777;">
        PQC-sealed • Fed directly into ROI calculator
      </div>
    </div>
  </div>

  <script>
    // === CHANGE THESE TWO LINES ONLY ===
    const BACKEND_URL = "https://YOUR_ACTUAL_DEPLOYED_URL.onrender.com";  // ← Put your Render/Railway URL here
    const API_KEY = "sk-ace-demo-key-001";                               // ← Your API key from dashboard

    async function classifyTransaction() {
      const narrative = document.getElementById('narrative').value.trim();
      if (!narrative) return alert("Please enter a transaction narrative");

      const resultDiv = document.getElementById('result');
      resultDiv.style.display = 'block';

      try {
        const res = await fetch(`${BACKEND_URL}/temenos_classify`, {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${API_KEY}`,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ narrative })
        });

        if (!res.ok) throw new Error("Server error");

        const data = await res.json();

        document.getElementById('classified-text').innerHTML = 
          `<strong>Original:</strong> ${data.original_narrative}<br><strong>Parsed by Temenos GenAI</strong>`;

        document.getElementById('sector-tag').textContent = data.classified_sector;
        document.getElementById('roi-impact').textContent = data.roi_impact;

      } catch (err) {
        document.getElementById('classified-text').innerHTML = 
          `<span style="color:#ff0055">❌ Could not connect to backend.<br>Please deploy your server first.</span>`;
        console.error(err);
      }
    }
  </script>
</body>
</html>
