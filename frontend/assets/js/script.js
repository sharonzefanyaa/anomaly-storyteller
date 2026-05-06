// =========================
// GLOBAL STATE
// =========================
let currentData = null;


// =========================
// NAVIGATION
// =========================
function goNext() {
  window.location.href = "options.html";
}

function autoMode() {
  window.location.href = "auto.html";
}

function manualMode() {
  window.location.href = "manual.html";
}


// =========================
// UTIL: SEND TO N8N
// =========================
function sendToN8N(payload = null) {

  const data = payload || currentData;

  if (!data) {
    alert("No data to send!");
    return;
  }

  fetch("http://127.0.0.1:5000/send", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
    .then(res => res.json())
    .then(res => {
      console.log("SENT:", res);
      alert("Data submitted!");
    })
    .catch(err => {
      console.error("SEND ERROR:", err);
      alert("Failed to submit data");
    });
}


// =========================
// AUTO PAGE INIT
// =========================
function initAutoPage() {

  const status = document.getElementById("status");
  const preview = document.getElementById("preview");

  if (!status || !preview) return;

  fetch("http://127.0.0.1:5000/auto", {
    method: "POST"
  })
    .then(res => res.json())
    .then(res => {

      const data = res.data;
      currentData = data;

      setTimeout(() => {

        status.innerHTML = `Data generated at ${data.datetime}`;
        status.classList.add("success");

        preview.innerHTML = renderPreview(data);

      }, 500);

    })
    .catch(err => {
      console.error(err);
      status.innerHTML = "Failed to generate data";
      status.classList.add("error");
    });
}


// =========================
// MANUAL SUBMIT (generate + send)
// =========================
function submitData() {

  const data = {
    platform: getVal("platform"),
    campaign_name: getVal("campaign_name"),
    campaign_status: getVal("campaign_status"),
    creative_type: getVal("creative_type"),
    audience_type: getVal("audience_type"),
    impressions: getVal("impressions"),
    clicks: getVal("clicks"),
    registrations: getVal("registrations"),
    cost: getVal("cost"),
    frequency: getVal("frequency")
  };

  // langsung send
  sendToN8N(data);
}


// =========================
// HELPERS
// =========================
function getVal(id) {
  const el = document.getElementById(id);
  return el ? el.value : "";
}


// =========================
// RENDER PREVIEW UI
// =========================
function renderPreview(data) {

  return `
    <div class="preview">

      <div class="preview-title">Preview Data</div>

      <table>
        <tbody>
          <tr><td>Platform</td><td>${data.platform || "-"}</td></tr>
          <tr><td>Campaign</td><td>${data.campaign_name || "-"}</td></tr>
          <tr><td>Status</td><td>${data.campaign_status || "-"}</td></tr>
          <tr><td>Creative</td><td>${data.creative_type || "-"}</td></tr>
          <tr><td>Audience</td><td>${data.audience_type || "-"}</td></tr>
          <tr><td>Impressions</td><td>${data.impressions ?? "-"}</td></tr>
          <tr><td>Clicks</td><td>${data.clicks ?? "-"}</td></tr>
          <tr><td>Registrations</td><td>${data.registrations ?? "-"}</td></tr>
          <tr><td>Cost</td><td>${data.cost ?? "-"}</td></tr>
          <tr><td>Frequency</td><td>${data.frequency ?? "-"}</td></tr>
        </tbody>
      </table>

      <button class="send-btn" onclick="sendToN8N()">
        Submit Data
      </button>

    </div>
  `;
}


// =========================
// AUTO INIT (SAFE)
// =========================
window.addEventListener("DOMContentLoaded", () => {

  // hanya jalan kalau ada auto page
  if (document.getElementById("status")) {
    initAutoPage();
  }

});