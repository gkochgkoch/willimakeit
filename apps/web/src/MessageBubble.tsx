import type { AssistantStatus } from './api'

interface MessageBubbleProps {
  status: AssistantStatus
  message: string | null
}

export function MessageBubble({ status, message }: MessageBubbleProps) {
  if (status === 'need_more_information') {
    return (
      <div className="rounded-xl border border-amber-200 bg-amber-50 p-5 text-base leading-relaxed text-amber-900">
        {message ?? 'More information is needed to assess this connection.'}
      </div>
    )
  }

  return (
    <div className="whitespace-pre-line rounded-xl border border-white/60 bg-white/80 p-5 text-base leading-relaxed text-slate-700 shadow-lg shadow-teal-900/5 backdrop-blur-sm">
      {message ?? 'No assessment message was returned.'}
    </div>
  )
}