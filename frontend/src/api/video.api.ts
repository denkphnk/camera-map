import { api } from "./axios";

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
    return api.get("/videos/me");
  },

  getVideoStreamUrl(
    videoId: string,
  ) {
    return `${
      import.meta.env.VITE_API_URL
    }/videos/${videoId}/stream`;
  },

  getPreviewUrl(
    videoId: string,
  ) {
    return `${
      import.meta.env.VITE_API_URL
    }/videos/${videoId}/preview`;
  },

  deleteVideo(videoId: string) {
  return api.delete(`/videos/${videoId}`);
  },
  
  getVideos() {
  return api.get("/videos");
  },
};

