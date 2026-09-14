import { useMutation, useQueryClient } from "@tanstack/react-query";

import { videoApi } from "../api/video.api";

export function useDeleteVideo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (videoId: string) =>
      videoApi.deleteVideo(videoId),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["videos"],
      });
    },
  });
}