import React from 'react';
import { createRoot } from 'react-dom/client';
import {
  approve,
  createSession,
  getBudget,
  getEvents,
  getModelHealth,
  getRuntimeStatus,
  reject,
  sendTurn,
  shutdownRuntime,
  speechStreamUrl,
  transcribeAudio,
  type Budget,
  type EventItem,
  type ModelHealth,
  type RuntimeStatus,
  type Session,
  type Turn
} from './lib/api';
import './styles.css';

type Message = { role: 'user' | 'assistant' | 'system'; text: string };
type InputMode = 'text' | 'voice';

function VoiceCore({ status }: { status: string }) {
  const state =
    status === 'awaiting_approval'
      ? 'Needs approval'
      : status === 'sending'
        ? 'Thinking'
        : status === 'listening'
          ? 'Listening'
          : 'Ready';

  return (
    <section className={`voice-core ${status}`}>
      <div className="core-visual">
        <div className="ring ring-outer" />
        <div className="ring ring-mid" />
        <div className="ring ring-inner" />
        <div className="core-dot" />
      </div>
      <div className="voice-copy">
        <h1>{state}</h1>
        <p>JARVIS Voice Layer on OpenClaw. STT/TTS here, execution and approvals in OpenClaw.</p>
      </div>
    </section>
  );
}

function App() {
  const [session, setSession] = React.useState<Session | null>(null);
  const [input, setInput] = React.useState('');
  const [messages, setMessages] = React.useState<Message[]>([{ role: 'system', text: 'JARVIS initializing local session...' }]);
  const [events, setEvents] = React.useState<EventItem[]>([]);
  const [budget, setBudget] = React.useState<Budget | null>(null);
  const [modelHealth, setModelHealth] = React.useState<ModelHealth | null>(null);
  const [runtimeStatus, setRuntimeStatus] = React.useState<RuntimeStatus | null>(null);
  const [lastTurn, setLastTurn] = React.useState<Turn | null>(null);
  const [status, setStatus] = React.useState('idle');
  const [runtimeMessage, setRuntimeMessage] = React.useState('Runtime controls ready.');
  const [voiceEnabled, setVoiceEnabled] = React.useState(true);
  const [micMessage, setMicMessage] = React.useState('Mic ready.');
  const [chatOpen, setChatOpen] = React.useState(false);
  const mediaRecorderRef = React.useRef<MediaRecorder | null>(null);
  const audioChunksRef = React.useRef<Blob[]>([]);
  const responseAudioRef = React.useRef<HTMLAudioElement | null>(null);
  const messagesRef = React.useRef<HTMLDivElement | null>(null);

  React.useEffect(() => {
    createSession()
      .then((s) => {
        setSession(s);
        setMessages([{ role: 'system', text: `Session ready: ${s.id}` }]);
      })
      .catch((error) => setMessages([{ role: 'system', text: String(error) }]));
  }, []);

  React.useEffect(() => {
    messagesRef.current?.scrollTo({ top: messagesRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages, chatOpen]);

  const refresh = React.useCallback(async () => {
    if (!session) return;
    const [nextEvents, nextBudget, nextModelHealth, nextRuntimeStatus] = await Promise.all([
      getEvents(session.id),
      getBudget(),
      getModelHealth(),
      getRuntimeStatus()
    ]);
    setEvents(nextEvents.slice(-8).reverse());
    setBudget(nextBudget);
    setModelHealth(nextModelHealth);
    setRuntimeStatus(nextRuntimeStatus);
  }, [session]);

  React.useEffect(() => {
    void refresh();
  }, [refresh, lastTurn]);

  async function speak(text: string) {
    const spokenText = text
      .replace(/\*\*([^*]+)\*\*/g, '$1')
      .replace(/\*([^*]+)\*/g, '$1')
      .replace(/`([^`]+)`/g, '$1')
      .replace(/^\s*[-*]\s+/gm, '')
      .replace(/^\s*\d+\.\s+/gm, '')
      .replace(/\s+/g, ' ')
      .trim();
    if (!spokenText) return;
    if (!voiceEnabled) return;
    window.speechSynthesis?.cancel();
    responseAudioRef.current?.pause();

    try {
      const audio = new Audio(speechStreamUrl(spokenText));
      audio.preload = 'auto';
      responseAudioRef.current = audio;
      await audio.play();
    } catch {
      if (!('speechSynthesis' in window)) return;
      const utterance = new SpeechSynthesisUtterance(spokenText);
      utterance.lang = 'ko-KR';
      utterance.rate = 0.96;
      utterance.pitch = 0.82;
      window.speechSynthesis.speak(utterance);
    }
  }

  async function submitText(text: string, mode: InputMode = 'text') {
    if (!session || !text.trim()) return;
    const cleanText = text.trim();
    setInput('');
    setStatus('sending');
    setMessages((current) => [...current, { role: 'user', text: cleanText }]);
    try {
      const turn = await sendTurn(session.id, cleanText, mode);
      setLastTurn(turn);
      setStatus(turn.status);
      const assistantText = turn.final_response ?? `Turn status: ${turn.status}`;
      setMessages((current) => [...current, { role: 'assistant', text: assistantText }]);
      if (turn.requires_approval) {
        void speak('승인이 필요한 작업입니다. 화면의 승인 카드를 확인해 주세요.');
      } else if (turn.status === 'blocked') {
        void speak(assistantText);
      } else {
        void speak(assistantText);
      }
    } catch (error) {
      setStatus('error');
      setMessages((current) => [...current, { role: 'assistant', text: String(error) }]);
    }
  }

  async function submit() {
    await submitText(input);
  }

  async function resolveApproval(action: 'approve' | 'reject') {
    if (!lastTurn?.approval_id) return;
    setStatus('sending');
    try {
      const result = action === 'approve' ? await approve(lastTurn.approval_id) : await reject(lastTurn.approval_id);
      const turn = result && typeof result === 'object' && 'turn' in result ? (result as { turn?: Turn }).turn : undefined;
      const message = action === 'approve'
        ? (turn?.final_response ?? '승인된 작업 처리가 끝났습니다.')
        : '거절했습니다. 실행된 작업은 없습니다.';
      setLastTurn(turn ?? null);
      setStatus(turn?.status ?? 'idle');
      setMessages((current) => [...current, { role: 'assistant', text: message }]);
      void speak(message);
      await refresh();
    } catch (error) {
      setStatus('error');
      setMessages((current) => [...current, { role: 'assistant', text: String(error) }]);
    }
  }

  async function stopRuntime(target: 'voice_api' | 'frontend' | 'ollama') {
    const labels = { voice_api: 'JARVIS Voice Layer API', frontend: 'Frontend dev server', ollama: 'Ollama' };
    const ok = window.confirm(`${labels[target]}를 종료할까요?`);
    if (!ok) return;
    setRuntimeMessage(`Stopping ${labels[target]}...`);
    try {
      const result = await shutdownRuntime([target]);
      setRuntimeMessage(result.results.map((item) => `${item.target}: ${item.status}`).join(' | '));
      if (target !== 'voice_api') {
        await refresh();
      }
    } catch (error) {
      setRuntimeMessage(String(error));
    }
  }

  async function startMic() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream, { mimeType: MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : undefined });
      mediaRecorderRef.current = recorder;
      audioChunksRef.current = [];
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) audioChunksRef.current.push(event.data);
      };
      recorder.onstop = () => {
        stream.getTracks().forEach((track) => track.stop());
        const audio = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        audioChunksRef.current = [];
        void submitRecordedAudio(audio);
      };
      recorder.start();
      setStatus('listening');
      setMicMessage('Recording. Press STOP when done.');
    } catch (error) {
      setStatus('error');
      setMicMessage(`Microphone failed: ${String(error)}`);
    }
  }

  async function submitRecordedAudio(audio: Blob) {
    if (!audio.size) {
      setStatus('idle');
      setMicMessage('No audio captured.');
      return;
    }
    setStatus('sending');
    setMicMessage('Transcribing voice prompt...');
    try {
      const transcription = await transcribeAudio(audio);
      if (!transcription.text.trim()) {
        setStatus('idle');
        setMicMessage('No speech detected.');
        return;
      }
      setMicMessage(`Prompt: ${transcription.text}`);
      await submitText(transcription.text, 'voice');
    } catch (error) {
      setStatus('error');
      setMicMessage(`STT failed: ${String(error)}`);
    }
  }

  async function toggleMic() {
    if (status === 'listening') {
      mediaRecorderRef.current?.stop();
      return;
    }
    await startMic();
  }

  const runtimeByName = React.useMemo(() => {
    const map = new Map<string, boolean>();
    runtimeStatus?.services.forEach((service) => map.set(service.name, service.running));
    return map;
  }, [runtimeStatus]);

  return (
    <main className="app-shell">
      <header className="top-bar">
        <strong>JARVIS</strong>
        <span>{modelHealth?.providers.find((provider) => provider.available)?.name.toUpperCase() ?? 'LOCAL READY'}</span>
        <span>{session ? session.id : 'creating session'}</span>
        <span>{budget ? `BUDGET ${Math.round((budget.estimated_cost_krw / budget.monthly_budget_krw) * 100)}%` : 'BUDGET --'}</span>
        <button className="top-action" onClick={() => setChatOpen(true)}>CHAT</button>
      </header>

      <div className="hud-grid">
        <aside className="telemetry panel">
          <h2>OPENCLAW RUNTIME</h2>
          <p>OpenClaw: {runtimeByName.get('openclaw') ? 'ready' : 'not linked'}</p>
          <p>Voice Layer: {runtimeByName.get('voice_api') ? 'ready' : 'offline'}</p>
          <p>Model: {modelHealth?.providers.find((provider) => provider.available)?.name ?? 'checking'}</p>
          <p>Ollama: {modelHealth?.providers.find((provider) => provider.name === 'ollama')?.available ? 'ready' : 'offline'}</p>
          <div className="mini-gauge">
            {budget?.local_model_calls ?? 0}
            <small>local calls</small>
          </div>
        </aside>

        <div className="center-stage">
          <VoiceCore status={status} />
          <div className="transcript panel">
            <span>{messages[messages.length - 1]?.text ?? 'Ready.'}</span>
          </div>
          <div className="quick-actions">
            <button onClick={() => void toggleMic()}>{status === 'listening' ? 'STOP' : 'MIC'}</button>
            <button onClick={() => setChatOpen(true)}>CHAT</button>
          </div>
        </div>

        <aside className="session panel">
          <h2>SESSION</h2>
          <p>Mode: OpenClaw + Voice Layer</p>
          <p>Input: mic transcript and chat popup</p>
          <p>Approval: OpenClaw-owned</p>
          <p>Finance: read-only briefings</p>

          <div className="voice-controls">
            <div className="runtime-line">
              <span>Voice output</span>
              <strong>{voiceEnabled ? 'on' : 'off'}</strong>
            </div>
            <div className="runtime-line">
              <span>TTS</span>
              <strong>neural</strong>
            </div>
            <button onClick={() => setVoiceEnabled((enabled) => !enabled)} title="Toggle spoken assistant responses">
              {voiceEnabled ? 'MUTE' : 'SPEAK'}
            </button>
            <p className="runtime-message">{micMessage}</p>
          </div>

          <div className="runtime-control">
            <h2>RUNTIME CONTROL</h2>
            <div className="runtime-line"><span>OpenClaw</span><strong>{runtimeByName.get('openclaw') ? 'on' : 'off'}</strong></div>
            <div className="runtime-line"><span>Voice API</span><strong>{runtimeByName.get('voice_api') ? 'on' : 'off'}</strong></div>
            <div className="runtime-line"><span>UI</span><strong>{runtimeByName.get('frontend') ? 'on' : 'off'}</strong></div>
            <div className="runtime-line"><span>Ollama</span><strong>{runtimeByName.get('ollama') ? 'on' : 'off'}</strong></div>
            <div className="runtime-actions">
              <button onClick={() => void stopRuntime('ollama')} title="Stop Ollama local model runtime">OLLAMA</button>
              <button onClick={() => void stopRuntime('frontend')} title="Stop Vite frontend dev server">UI</button>
              <button onClick={() => void stopRuntime('voice_api')} title="Stop JARVIS Voice Layer API">VOICE</button>
            </div>
            <p className="runtime-message">{runtimeMessage}</p>
          </div>
        </aside>
      </div>

      <section className="activity-row">
        <aside className={`activity panel ${lastTurn?.requires_approval ? 'approval' : ''}`}>
          <h2>{lastTurn?.requires_approval ? 'APPROVAL REQUIRED' : 'ACTIVITY'}</h2>
          {lastTurn?.requires_approval ? (
            <div className="approval-card">
              <p>Risk: {lastTurn.risk_level}</p>
              <p>Turn: {lastTurn.id}</p>
              <div className="approval-actions">
                <button onClick={() => void resolveApproval('approve')}>Approve</button>
                <button onClick={() => void resolveApproval('reject')}>Reject</button>
              </div>
            </div>
          ) : null}
          <div className="events">
            {events.map((event) => (
              <div className="event" key={event.id} title={JSON.stringify(event.payload)}>
                <span className="event-name">{event.event_type}</span>
                <span className="event-risk">{event.risk_level ?? 'none'}</span>
              </div>
            ))}
          </div>
        </aside>
      </section>

      {chatOpen ? (
        <div className="chat-overlay" role="dialog" aria-modal="true">
          <section className="chat-modal panel">
            <div className="modal-head">
              <h2>CHAT CONSOLE</h2>
              <button onClick={() => setChatOpen(false)}>CLOSE</button>
            </div>
            <div className="messages" ref={messagesRef}>
              {messages.map((message, index) => (
                <div key={index} className={`message ${message.role}`}>{message.text}</div>
              ))}
            </div>
            <div className="input-row">
              <input
                autoFocus
                value={input}
                onChange={(event) => setInput(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === 'Enter') void submit();
                  if (event.key === 'Escape') setChatOpen(false);
                }}
                placeholder="Type a command or edit the last transcript..."
              />
              <button onClick={() => void toggleMic()}>{status === 'listening' ? 'STOP' : 'MIC'}</button>
              <button onClick={() => void submit()}>SEND</button>
            </div>
          </section>
        </div>
      ) : null}
    </main>
  );
}

createRoot(document.getElementById('root')!).render(<App />);
