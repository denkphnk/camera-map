import { useQuery } from "@tanstack/react-query";

import { cameraApi } from "../api/camera.api";

import type { GeoJsonResponse } from "../types/camera.types";

export function useGeoJson() {
  return useQuery<GeoJsonResponse>({
    queryKey: ["geojson"],

    queryFn: async () => {
      const response =
        await cameraApi.getGeoJson();

      return response.data;
    },
  });
}