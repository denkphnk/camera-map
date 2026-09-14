export interface Video {
  id: string;
  name: string;
  duration: number;
  video_resolution: string;
  fps: number;
  time_of_day: string;
  tracing: string;
  author_id: string;
  counter: number;
  file_size: number;
  content_type: string;
  created_at: string;
}

export interface VideoListResponse {
  items: Video[];
  total: number;
}