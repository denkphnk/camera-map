import type { Video } from "./video.types";

export interface CameraDetails {
  id: string;
  camera_id: string;
  camera_name: string;
  camera_place: string | null;
  camera_place_cd: number | null;

  camera_latitude: number;
  camera_longitude: number;

  camera_type: string | null;
  camera_type_cd: number | null;

  camera_class: string | null;
  camera_class_cd: number | null;

  model: string | null;
  serial_number: string | null;

  azimuth: number | null;
  archive: number;

  process_dttm: string;

  video_count: number | null;
}

export interface CameraDetailsResponse {
  camera: CameraDetails;
  videos: Video[];
  total: number;
}