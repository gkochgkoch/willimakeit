import ReactMarkdown from 'react-markdown'
import type { AssistantStatus } from './api'

interface MessageBubbleProps {
  status: AssistantStatus
  message: string | null
}

export function MessageBubble({ status, message }: MessageBubbleProps) {
  if (status === 'need_more_information') {
    return (
      <div className="markdown-content rounded-xl border border-amber-200 bg-amber-50 p-5 text-base leading-relaxed text-amber-900">
        <ReactMarkdown>{message ?? ''}</ReactMarkdown>
      </div>
    )
  }

  return (
    <div className="markdown-content rounded-xl border border-white/60 bg-white/80 p-5 text-base leading-relaxed text-slate-700 shadow-lg shadow-teal-900/5 backdrop-blur-sm">
      {message === null && <p>No assessment message was returned.</p>}
      {message !== null && <ReactMarkdown>{message}</ReactMarkdown>}
    </div>
  )
}