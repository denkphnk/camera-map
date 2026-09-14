import { useQuery } from "@tanstack/react-query";

import { cameraApi } from "../api/camera.api";

import type { CameraDetailsResponse } from "../types/camera-details.types";

export function useCameraDetails(
  cameraId: string,
) {
  return useQuery<CameraDetailsResponse>({
    queryKey: [
      "camera-details",
      cameraId,
    ],

    queryFn: async () => {
      const response =
        await cameraApi.getCameraDetails(
          cameraId,
        );

      return response.data;
    },

    enabled: !!cameraId,
  });
}