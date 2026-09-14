import { useQuery } from "@tanstack/react-query";

import { videoApi } from "../api/video.api";

import type { VideoListResponse } from "../types/video.types";

export function useAllVideos() {
  return useQuery<VideoListResponse>({
    queryKey: ["videos"],

    queryFn: async () => {
      const response =
        await videoApi.getVideos();

      return response.data;
    },
  });
}