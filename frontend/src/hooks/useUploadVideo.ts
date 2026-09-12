import { useMutation } from "@tanstack/react-query";

import { videoApi } from "../api/video.api";

export function useUploadVideo() {
  return useMutation({
    mutationFn:
      videoApi.upload,
  });
}