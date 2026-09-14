export interface Video {
  id: string;
  name: string;
  duration: number;
  video_resolution: string;
  fps: number;
  tracing: string;
  counter: number;
  created_at: string;
  video_url: string;
  preview_url: string;
  author_name: string;
}

export interface VideoListResponse {
  items: Video[];
  total: number;
}