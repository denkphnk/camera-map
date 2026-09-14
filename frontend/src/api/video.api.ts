import { api } from "./axios";

import type {
  VideoListResponse,
} from "../types/video.types";

export const videoApi = {
  upload(
    file: File,
    cameraId: string,
  ) {
    const formData =
      new FormData();

    formData.append(
      "file",
      file,
    );

    formData.append(
      "name",
      file.name,
    );

    formData.append(
      "camera_id",
      cameraId,
    );

    return api.post(
      "/videos/upload",
      formData,
      {
        headers: {
          "Content-Type":
            "multipart/form-data",
        },
      },
    );
  },

  getMyVideos() {
    return api.get<VideoListResponse>(
      "/videos",
      {
        params: {
          limit: 100,
        },
      },
    );
  },
};