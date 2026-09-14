import { useQuery } from "@tanstack/react-query";

import { videoApi } from "../api/video.api";

export function useVideos() {
  return useQuery({
    queryKey: ["videos"],

    queryFn: async () => {
      const response =
        await videoApi.getMyVideos();

      return response.data;
    },
  });
}