export type AnalysisStatus =
  | "queued"
  | "processing"
  | "done"
  | "error";

export interface Analysis {
  id: string;
  video_id: string;

  video_name: string;
  camera_name: string;

  status: AnalysisStatus;

  result: Record<string, unknown> | null;
  error_message: string | null;

  created_at: string;
  started_at: string | null;
  finished_at: string | null;
}

export interface AnalysisListResponse {
  items: Analysis[];
}

export interface AnalysisFilters {
  status?: string;
  created_from?: string;
  created_to?: string;
}

