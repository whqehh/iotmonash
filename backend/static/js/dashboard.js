let telemetryChart = null;
let currentChartMetric = 'all';
let currentActuators = {};

const CHART_COLORS = {
  soil_moisture: { border: '#10b981', bg: 'rgba(16, 185, 129, 0.15)' },
  water_level:   { border: '#06b6d4', bg: 'rgba(6, 182, 212, 0.15)' },
  temperature:   { border: '#f59e0b', bg: 'rgba(245, 158, 11, 0.15)' },
  humidity:      { border: '#ec4899', bg: 'rgba(236, 72, 153, 0.15)' }
};

document.addEventListener('DOMContentLoaded', () => {
  initChart();
  fetchLatestSensors();
  fetchActuatorStates();
  fetchSensorHistory();
  fetchAuditLogs();

  setInterval(fetchLatestSensors, 3500);
  setInterval(fetchActuatorStates, 3000);
  setInterval(fetchSensorHistory, 6000);
  setInterval(fetchAuditLogs, 5000);

  const pollBtn = document.getElementById('poll-now-btn');
  if (pollBtn) {
    pollBtn.addEventListener('click', triggerImmediatePoll);
  }
});

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerText = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.4s ease';
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 400);
  }, 4000);
}

async function fetchLatestSensors() {
  try {
    const res = await fetch('/api/sensors/latest');
    const data = await res.json();
    if (data.success && data.sensors) {
      updateSensorCards(data.sensors);
      const now = new Date();
      document.getElementById('last-update-time').innerText = now.toLocaleTimeString();
    }
  } catch (err) {
    console.warn('Sensor fetch error:', err);
  }
}

function updateSensorCards(sensors) {
  // 1. Soil Moisture (Threshold: < 500 -> Pump ON)
  if (sensors.soil_moisture) {
    const val = sensors.soil_moisture.value;
    document.getElementById('val-soil-moisture').innerText = val.toFixed(1);
    const pct = Math.min(100, Math.max(0, (val / 1023) * 100));
    document.getElementById('gauge-soil-moisture').style.width = `${pct}%`;
    const badge = document.getElementById('badge-soil-moisture');
    if (val < 500.0) {
      badge.className = 'sensor-state-badge badge-alert';
      badge.innerText = 'LOW (<500 PUMP ON)';
    } else {
      badge.className = 'sensor-state-badge badge-normal';
      badge.innerText = 'OPTIMAL (>=500)';
    }
  }

  // 2. Water Reservoir Level (Threshold: < 500 -> LED ON)
  if (sensors.water_level) {
    const val = sensors.water_level.value;
    document.getElementById('val-water-level').innerText = val.toFixed(1);
    const pct = Math.min(100, Math.max(0, (val / 1023) * 100));
    document.getElementById('gauge-water-level').style.width = `${pct}%`;
    const badge = document.getElementById('badge-water-level');
    if (val < 500.0) {
      badge.className = 'sensor-state-badge badge-danger';
      badge.innerText = 'LOW (<500 LED ON)';
    } else {
      badge.className = 'sensor-state-badge badge-normal';
      badge.innerText = 'OPTIMAL (>=500)';
    }
  }

  // 3. Temperature / Sensor (Threshold: > 300 -> Fan ON)
  if (sensors.temperature) {
    const val = sensors.temperature.value;
    document.getElementById('val-temperature').innerText = val.toFixed(1);
    const pct = Math.min(100, Math.max(0, (val / 1023) * 100));
    document.getElementById('gauge-temperature').style.width = `${pct}%`;
    const badge = document.getElementById('badge-temperature');
    if (val > 300.0) {
      badge.className = 'sensor-state-badge badge-alert';
      badge.innerText = 'HIGH (>300 FAN ON)';
    } else {
      badge.className = 'sensor-state-badge badge-normal';
      badge.innerText = 'NORMAL (<=300)';
    }
  }

  // 4. Humidity
  if (sensors.humidity) {
    const val = sensors.humidity.value;
    document.getElementById('val-humidity').innerText = val.toFixed(1);
    document.getElementById('gauge-humidity').style.width = `${Math.min(100, Math.max(0, val))}%`;
    const badge = document.getElementById('badge-humidity');
    if (val > 75.0) {
      badge.className = 'sensor-state-badge badge-alert';
      badge.innerText = 'HIGH';
    } else {
      badge.className = 'sensor-state-badge badge-normal';
      badge.innerText = 'BALANCED';
    }
  }
}

async function fetchActuatorStates() {
  try {
    const res = await fetch('/api/actuators');
    const data = await res.json();
    if (data.success && data.actuators) {
      currentActuators = data.actuators;
      renderActuatorTiles(data.actuators);
    }
  } catch (err) {
    console.warn('Actuator fetch error:', err);
  }
}

function renderActuatorTiles(actuators) {
  ['pump', 'fan', 'led'].forEach(act => {
    const item = actuators[act];
    if (!item) return;

    const lamp = document.getElementById(`lamp-${act}`);
    const stateVal = document.getElementById(`state-${act}`);
    const modeBadge = document.getElementById(`mode-${act}`);
    const reasonText = document.getElementById(`reason-${act}`);
    const toggleBtn = document.getElementById(`btn-toggle-${act}`);

    if (item.state) {
      lamp.className = act === 'led' ? 'relay-lamp active-red' : 'relay-lamp active-green';
      stateVal.innerText = 'ON';
      stateVal.style.color = act === 'led' ? '#ef4444' : '#10b981';
      toggleBtn.innerText = 'Turn OFF (Manual)';
    } else {
      lamp.className = 'relay-lamp';
      stateVal.innerText = 'OFF';
      stateVal.style.color = '#94a3b8';
      toggleBtn.innerText = 'Turn ON (Manual)';
    }

    modeBadge.innerText = item.mode;
    modeBadge.style.background = item.mode === 'MANUAL' ? 'rgba(245, 158, 11, 0.15)' : 'rgba(59, 130, 246, 0.15)';
    modeBadge.style.color = item.mode === 'MANUAL' ? '#f59e0b' : '#3b82f6';
    modeBadge.style.borderColor = item.mode === 'MANUAL' ? 'rgba(245, 158, 11, 0.3)' : 'rgba(59, 130, 246, 0.3)';

    reasonText.innerText = item.triggered_by || 'Awaiting conditions';
  });
}

async function toggleActuator(actuatorName) {
  const current = currentActuators[actuatorName];
  const newState = current ? !current.state : true;

  try {
    const res = await fetch('/api/actuators/control', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ actuator: actuatorName, state: newState })
    });

    const data = await res.json();
    if (res.ok && data.success) {
      showToast(`${actuatorName.toUpperCase()} manually switched ${newState ? 'ON' : 'OFF'}`, 'info');
      fetchActuatorStates();
    } else {
      showToast(`Error: ${data.error || 'Operation failed'}`, 'danger');
    }
  } catch (err) {
    showToast(`Network error controlling ${actuatorName}`, 'danger');
  }
}

async function setModeAuto(actuatorName) {
  try {
    const res = await fetch('/api/actuators/mode', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ actuator: actuatorName, mode: 'AUTO' })
    });
    const data = await res.json();
    if (data.success) {
      showToast(`${actuatorName.toUpperCase()} returned to Autonomous Mode`, 'info');
      fetchActuatorStates();
    }
  } catch (err) {
    console.error('Mode change error:', err);
  }
}

async function triggerImmediatePoll() {
  const btn = document.getElementById('poll-now-btn');
  btn.disabled = true;
  btn.innerHTML = 'Polling Sensors...';

  try {
    const res = await fetch('/api/sensors/poll-now', { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      showToast('Immediate poll completed & saved to MySQL sensor_data!', 'info');
      fetchLatestSensors();
      fetchActuatorStates();
      fetchSensorHistory();
      fetchAuditLogs();
    } else {
      showToast(`Polling rejected: ${data.error}`, 'warn');
    }
  } catch (err) {
    showToast('Failed to trigger poll', 'danger');
  } finally {
    setTimeout(() => {
      btn.disabled = false;
      btn.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
        Poll Sensors Now
      `;
    }, 1200);
  }
}

async function fetchAuditLogs() {
  try {
    const res = await fetch('/api/security/logs');
    const data = await res.json();
    if (data.success && data.logs) {
      const tbody = document.getElementById('audit-log-body');
      if (data.logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="table-placeholder">No security audit logs yet.</td></tr>';
        return;
      }

      tbody.innerHTML = data.logs.map(log => `
        <tr>
          <td style="font-family: var(--font-mono); color: var(--text-muted); font-size: 0.78rem;">${log.created_at || ''}</td>
          <td><strong>${escapeHtml(log.event_type)}</strong></td>
          <td><span class="severity-tag severity-${log.severity}">${log.severity}</span></td>
          <td>${escapeHtml(log.details)}</td>
          <td style="font-family: var(--font-mono); color: var(--text-muted); font-size: 0.78rem;">${escapeHtml(log.source_ip || '127.0.0.1')}</td>
        </tr>
      `).join('');
    }
  } catch (err) {
    console.warn('Audit fetch error:', err);
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function initChart() {
  const ctx = document.getElementById('telemetryChart');
  if (!ctx) return;

  telemetryChart = new Chart(ctx, {
    type: 'line',
    data: { labels: [], datasets: [] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: {
          labels: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', size: 12 } }
        },
        tooltip: {
          backgroundColor: 'rgba(14, 20, 34, 0.95)',
          titleColor: '#f1f5f9',
          bodyColor: '#cbd5e1',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          padding: 10
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 10 } }
        },
        y: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 10 } },
          min: 0,
          max: 1024
        }
      }
    }
  });
}

async function fetchSensorHistory() {
  try {
    const res = await fetch('/api/sensors/history?limit=40');
    const data = await res.json();
    if (data.success && data.history) {
      updateChartData(data.history);
    }
  } catch (err) {
    console.warn('Chart history error:', err);
  }
}

function updateChartData(historyRows) {
  if (!telemetryChart) return;

  const grouped = {};
  historyRows.forEach(row => {
    const timeLabel = row.created_at ? row.created_at.split(' ')[1] : '';
    if (!grouped[timeLabel]) grouped[timeLabel] = {};
    grouped[timeLabel][row.sensor_position] = row.sensor_value;
  });

  const labels = Object.keys(grouped).slice(-15);
  const metrics = currentChartMetric === 'all' 
    ? ['soil_moisture', 'water_level', 'temperature', 'humidity']
    : [currentChartMetric];

  const datasets = metrics.map(pos => {
    const config = CHART_COLORS[pos] || { border: '#fff', bg: 'rgba(255,255,255,0.1)' };
    const labelTitle = pos.replace('_', ' ').toUpperCase();
    return {
      label: labelTitle,
      data: labels.map(l => grouped[l] ? grouped[l][pos] || null : null),
      borderColor: config.border,
      backgroundColor: config.bg,
      fill: false,
      tension: 0.35,
      pointRadius: 3,
      pointHoverRadius: 6
    };
  });

  telemetryChart.data.labels = labels;
  telemetryChart.data.datasets = datasets;
  telemetryChart.update('none');
}

function switchChartMetric(metric) {
  currentChartMetric = metric;
  document.querySelectorAll('.chart-filter-pills .pill').forEach(p => p.classList.remove('active'));
  event.target.classList.add('active');
  fetchSensorHistory();
}
