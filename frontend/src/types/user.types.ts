export interface UserVideo {
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

export interface MeResponse {
  id: string;
  email: string;
  full_name: string;
  videos: UserVideo[];
  total_videos: number;
}