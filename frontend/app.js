const API_BASE = "http://127.0.0.1:8000/api/devices/PLANT-001";

// Chart initialization
const ctx = document.getElementById("moistureChart").getContext("2d");
const moistureChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [],
    datasets: [{
      label: "Soil Moisture (%)",
      data: [],
      borderColor: "#0284c7",
      backgroundColor: "rgba(2, 132, 199, 0.1)",
      fill: true,
      tension: 0.3,
      borderWidth: 2,
      pointRadius: 3
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: { min: 0, max: 100 }
    }
  }
});

async function fetchStatus() {
  try {
    const res = await fetch(`${API_BASE}/latest`);
    const data = await res.json();
    
    const onlineEl = document.getElementById("online-status");
    onlineEl.innerText = "Online";
    onlineEl.style.color = "#16a34a";
    
    if (data.reading) {
      document.getElementById("val-soil").innerText = data.reading.soil_moisture;
      document.getElementById("val-temp").innerText = data.reading.temperature;
      document.getElementById("val-hum").innerText = data.reading.humidity;
      
      const healthSub = document.getElementById("sub-health");
      if (data.reading.soil_moisture < data.threshold) {
        healthSub.innerText = "Needs Water";
        healthSub.style.color = "#dc2626";
      } else {
        healthSub.innerText = "Optimal";
        healthSub.style.color = "#16a34a";
      }
    }
    
    const pumpElem = document.getElementById("val-pump");
    const pumpSub = document.getElementById("pump-sub");
    if (data.pump_status) {
      pumpElem.innerText = "ON";
      pumpElem.style.color = "#16a34a";
      pumpSub.innerText = "Watering Active";
    } else {
      pumpElem.innerText = "OFF";
      pumpElem.style.color = "#0f172a";
      pumpSub.innerText = "Idle";
    }
  } catch (err) {
    const onlineEl = document.getElementById("online-status");
    onlineEl.innerText = "Offline";
    onlineEl.style.color = "#dc2626";
  }
}

async function updateChart() {
  try {
    const res = await fetch(`${API_BASE}/history?limit=10`);
    const json = await res.json();
    
    if (json.history && json.history.length > 0) {
      const labels = json.history.map(item => {
        const d = new Date(item.timestamp);
        return `${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')}:${String(d.getSeconds()).padStart(2, '0')}`;
      });
      const dataPoints = json.history.map(item => item.soil_moisture);
      
      moistureChart.data.labels = labels;
      moistureChart.data.datasets[0].data = dataPoints;
      moistureChart.update();
    }
  } catch (err) {
    console.error("Chart fetch error:", err);
  }
}

document.getElementById("btn-water").addEventListener("click", async () => {
  await fetch(`${API_BASE}/water`, { method: "POST" });
  fetchStatus();
});

document.getElementById("btn-save-thresh").addEventListener("click", async () => {
  const val = parseFloat(document.getElementById("input-threshold").value);
  await fetch(`${API_BASE}/threshold`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ moisture_threshold: val })
  });
  alert("Threshold updated to " + val + "%");
});

// Periodic updates
setInterval(() => {
  fetchStatus();
  updateChart();
}, 2500);

fetchStatus();
updateChart();