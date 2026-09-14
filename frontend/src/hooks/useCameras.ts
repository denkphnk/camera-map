import { useQuery } from "@tanstack/react-query";

import {
  cameraApi,
  type CameraFilters,
} from "../api/camera.api";

export function useCameras(
  filters: CameraFilters,
) {
  return useQuery({
    queryKey: [
      "cameras",
      filters,
    ],

    queryFn: async () => {
      const response =
        await cameraApi.getCameras(
          filters,
        );

      return response.data;
    },
  });
}