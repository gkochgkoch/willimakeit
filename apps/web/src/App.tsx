import { useRef, useState } from "react";
import type { KeyboardEvent } from "react";
import type { AssistantResponse, AssistantStatus } from "./api";
import { MessageBubble } from "./MessageBubble";

const API_URL = "http://localhost:8000/assistant/ask";

const EXAMPLES = ["Can I connect from LH123 to AF456 at CDG on 2026-08-15?"];

function SendIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      className="h-5 w-5"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="m22 2-7 20-4-9-9-4Z" />
      <path d="M22 2 11 13" />
    </svg>
  );
}

function ClearIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      className="h-5 w-5"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M18 6 6 18" />
      <path d="m6 6 12 12" />
    </svg>
  );
}

function Spinner() {
  return (
    <svg
      viewBox="0 0 24 24"
      className="h-5 w-5 animate-spin"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      aria-hidden="true"
    >
      <path d="M21 12a9 9 0 1 1-6.219-8.56" />
    </svg>
  );
}

function Skeleton() {
  return (
    <div aria-hidden="true" className="space-y-3.5">
      <div className="skeleton h-6 w-11/12 rounded-md" />
      <div className="skeleton h-6 w-full rounded-md" />
      <div className="skeleton h-6 w-3/4 rounded-md" />
      <div className="skeleton h-6 w-1/2 rounded-md" />
    </div>
  );
}

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastPrompt, setLastPrompt] = useState<string | null>(null);
  const [status, setStatus] = useState<AssistantStatus | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const textareaRef = useRef<HTMLTextAreaElement>(null);

  function resizeTextarea() {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 240)}px`;
  }

  function clearPrompt() {
    setPrompt("");
    requestAnimationFrame(() => {
      const el = textareaRef.current;
      if (el) {
        el.style.height = "auto";
        el.focus();
      }
    });
  }

  async function ask() {
    const question = prompt.trim();
    if (!question || loading) return;

    setLoading(true);
    setError(null);
    setLastPrompt(question);
    setStatus(null);
    setMessage(null);
    setPrompt("");
    requestAnimationFrame(resizeTextarea);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: question }),
      });

      if (!response.ok) {
        const body = (await response.json().catch(() => null)) as {
          detail?: string;
        } | null;
        setError(
          body?.detail ?? `Request failed with status ${response.status}.`,
        );
        return;
      }

      const data = (await response.json()) as AssistantResponse;
      setStatus(data.status);
      setMessage(data.message);
    } catch {
      setError("Could not reach the API. Is the backend running on port 8000?");
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void ask();
    }
  }

  const showEmptyState = !loading && lastPrompt === null;

  return (
    <div className="relative flex min-h-screen flex-col overflow-x-hidden">
      <div
        aria-hidden="true"
        className="animated-gradient fixed inset-0 -z-10"
      />

      <header className="w-full px-4 pt-24 sm:pt-28">
        <h1 className="text-center text-3xl font-bold tracking-tight text-teal-800 sm:text-4xl">
          Flight Connection Checker
        </h1>
      </header>

      <main className="flex flex-1 flex-col px-4">
        <div className="mx-auto flex w-full max-w-3xl flex-1 flex-col">
          <div className="pt-10 sm:pt-12">
            <div className="rounded-2xl border border-white/60 bg-white/80 p-5 shadow-lg shadow-teal-900/5 backdrop-blur-sm focus-within:border-pink-300 focus-within:shadow-pink-200/40">
              <textarea
                ref={textareaRef}
                value={prompt}
                onChange={(e) => {
                  setPrompt(e.target.value);
                  resizeTextarea();
                }}
                onKeyDown={handleKeyDown}
                rows={1}
                placeholder="Ask about your flight connection or baggage rules..."
                autoFocus
                className="max-h-[240px] w-full resize-none px-2 py-1 text-xl leading-8 text-slate-900 placeholder:text-slate-400 focus:outline-none"
              />
              <div className="flex items-center gap-1 pt-2">
                <div className="no-scrollbar flex min-w-0 flex-1 gap-1.5 overflow-x-auto">
                  {showEmptyState &&
                    EXAMPLES.map((example) => (
                      <button
                        key={example}
                        type="button"
                        onClick={() => {
                          setPrompt(example);
                          requestAnimationFrame(() => {
                            resizeTextarea();
                            textareaRef.current?.focus();
                          });
                        }}
                        className="flex cursor-pointer items-center gap-1.5 whitespace-nowrap rounded-full border border-slate-300/70 bg-white/70 px-3 py-1.5 text-xs text-slate-600 transition-colors hover:border-slate-400 hover:bg-white hover:text-slate-800"
                      >
                        <span className="text-[10px] font-semibold uppercase tracking-wide text-teal-700">
                          Example
                        </span>
                        {example}
                      </button>
                    ))}
                </div>
                {prompt.length > 0 && (
                  <button
                    type="button"
                    onClick={clearPrompt}
                    title="Clear"
                    aria-label="Clear input"
                    className="rounded-full p-3 text-slate-400 transition-colors hover:bg-pink-50 hover:text-pink-600"
                  >
                    <ClearIcon />
                  </button>
                )}
                <button
                  type="button"
                  onClick={() => void ask()}
                  disabled={!prompt.trim() || loading}
                  title="Send"
                  aria-label="Send message"
                  className="rounded-full bg-gradient-to-r from-pink-500 to-rose-500 p-3 text-white shadow-md shadow-pink-500/30 transition-colors hover:from-pink-600 hover:to-rose-600 disabled:cursor-not-allowed disabled:from-slate-200 disabled:to-slate-200 disabled:text-slate-400 disabled:shadow-none"
                >
                  {loading ? <Spinner /> : <SendIcon />}
                </button>
              </div>
            </div>
            {showEmptyState && (
              <p className="mt-3 text-center text-sm text-teal-900/70">
                Ask about a flight connection in your own words — the assistant
                will check flights, transfers, weather, and airline rules for
                you.
              </p>
            )}
          </div>

          <section aria-live="polite" className="pt-6">
            {!loading && error && (
              <div
                role="alert"
                className="rounded-xl border border-red-200 bg-red-50 p-5 text-base leading-relaxed text-red-700"
              >
                {error}
              </div>
            )}

            {!loading && !error && status !== null && (
              <MessageBubble status={status} message={message} />
            )}

            {loading && (
              <div className="rounded-xl border border-white/60 bg-white/80 p-5 shadow-lg shadow-teal-900/5 backdrop-blur-sm">
                <Skeleton />
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  );
}
