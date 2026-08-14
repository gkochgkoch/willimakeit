export type AssistantStatus = 'completed' | 'need_more_information'

export interface AssistantResponse {
  status: AssistantStatus
  assessment_id: string | null
  message: string | null
}