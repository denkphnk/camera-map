import { api } from "./axios";

export interface CameraFilters {
  search?: string;
  model?: string;
  camera_type?: string;
  camera_class?: string;
  video_count_from?: number;
  video_count_to?: number;
}

export const cameraApi = {
  getGeoJson() {
    return api.get(
      "/cameras/geojson",
    );
  },

  getCameras(
    filters?: CameraFilters,
  ) {
    return api.get("/cameras", {
      params: filters,
    });
  },
  getCameraDetails(cameraId: string) {
  return api.get(
    `/cameras/${cameraId}/details`,
  );
  },
};

