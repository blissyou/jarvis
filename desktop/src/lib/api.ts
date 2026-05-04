export type Session = {
  id: string;
  workspace_root: string | null;
  status: string;
  created_at: string;
};

export type Turn = {
  id: string;
  session_id: string;
  mode: string;
  risk_level: string;
  requires_approval: boolean;
  status: string;
  final_response: string | null;
  approval_id: string | null;
};

export type EventItem = {
  id: string;
  event_type: string;
  risk_level: string | null;
  payload: Record<string, unknown>;
  created_at: string;
};

export type ModelProviderHealth = {
  name: string;
  available: boolean;
  base_url: string | null;
  model: string | null;
  detail: string;
};

export type ModelHealth = {
  status: string;
  providers: ModelProviderHealth[];
};

export type Budget = {
  monthly_budget_krw: number;
  estimated_cost_krw: number;
  cloud_model_calls: number;
  local_model_calls: number;
  tool_calls: number;
  approval_requests: number;
};

export type RuntimeServiceStatus = {
  name: 'api' | 'frontend' | 'ollama' | string;
  running: boolean;
  detail: string;
};

export type RuntimeStatus = {
  services: RuntimeServiceStatus[];
};

export type RuntimeShutdownResult = {
  target: string;
  status: 'scheduled' | 'stopped' | 'not_running' | 'failed' | 'blocked';
  detail: string;
};

export type RuntimeShutdown = {
  results: RuntimeShutdownResult[];
};

export type Transcription = {
  text: string;
  language: string | null;
  duration_seconds: number | null;
};

const API_BASE = import.meta.env.VITE_JARVIS_API ?? 'http://127.0.0.1:8000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {})
    }
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${text}`);
  }
  return res.json() as Promise<T>;
}

export function createSession(workspaceRoot?: string) {
  return request<Session>('/sessions', {
    method: 'POST',
    body: JSON.stringify({ workspace_root: workspaceRoot ?? null })
  });
}

export function sendTurn(sessionId: string, text: string) {
  return request<Turn>(`/sessions/${sessionId}/turns`, {
    method: 'POST',
    body: JSON.stringify({
      input: { mode: 'text', text },
      workspace: { cwd: null, selected_files: [] },
      policy: { approval_mode: 'ask', cloud_allowed: false, network_allowed: 'ask' }
    })
  });
}

export function getEvents(sessionId: string) {
  return request<EventItem[]>(`/sessions/${sessionId}/events`);
}

export function getBudget() {
  return request<Budget>('/budgets/current');
}

export function getModelHealth() {
  return request<ModelHealth>('/models/health');
}

export function getRuntimeStatus() {
  return request<RuntimeStatus>('/runtime/status');
}

export function shutdownRuntime(targets: Array<'api' | 'frontend' | 'ollama'>) {
  return request<RuntimeShutdown>('/runtime/shutdown', {
    method: 'POST',
    body: JSON.stringify({ targets })
  });
}

export function approve(approvalId: string) {
  return request(`/approvals/${approvalId}/approve`, { method: 'POST' });
}

export function reject(approvalId: string) {
  return request(`/approvals/${approvalId}/reject`, { method: 'POST' });
}

export async function transcribeAudio(audio: Blob) {
  const form = new FormData();
  form.append('audio', audio, 'prompt.webm');
  const res = await fetch(`${API_BASE}/voice/transcribe`, {
    method: 'POST',
    body: form
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${text}`);
  }
  return res.json() as Promise<Transcription>;
}

export async function synthesizeSpeech(text: string) {
  const res = await fetch(`${API_BASE}/voice/speak`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`${res.status} ${errorText}`);
  }
  return res.blob();
}

export function speechStreamUrl(text: string) {
  return `${API_BASE}/voice/speak/stream?text=${encodeURIComponent(text)}`;
}
