import { useQuery } from "@tanstack/react-query";

import { videoApi } from "../api/video.api";

import type {
  VideoListResponse,
} from "../types/video.types";

export function useVideos() {
  return useQuery<VideoListResponse>({
    queryKey: ["videos"],

    queryFn: async () => {
      const response =
        await videoApi.getMyVideos();

      return response.data;
    },
  });
}