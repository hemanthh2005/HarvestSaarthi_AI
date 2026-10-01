/**
 * HarvestSaarthi AI - API Service Layer
 */

const API_BASE = '/api';

export async function fetchHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    return await res.json();
  } catch (err) {
    return { success: false, error: err.message };
  }
}

export async function fetchCrops() {
  try {
    const res = await fetch(`${API_BASE}/crops`);
    return await res.json();
  } catch (err) {
    return { success: false, data: ["Tomato", "Onion", "Banana", "Potato", "Green Chili"] };
  }
}

export async function postDecision(situation) {
  try {
    const res = await fetch(`${API_BASE}/decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(situation),
    });
    return await res.json();
  } catch (err) {
    return { success: false, error: err.message };
  }
}

export async function postWhatIf(requestData) {
  try {
    const res = await fetch(`${API_BASE}/what-if`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestData),
    });
    return await res.json();
  } catch (err) {
    return { success: false, error: err.message };
  }
}

export async function fetchDemoScenario(demoId) {
  try {
    const res = await fetch(`${API_BASE}/demo/${demoId}`);
    return await res.json();
  } catch (err) {
    return { success: false, error: err.message };
  }
}

export function getReportDownloadUrl(runId) {
  return `${API_BASE}/report/${runId || 'latest'}`;
}
