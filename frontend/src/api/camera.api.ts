import { api } from "./axios";

export const cameraApi = {
  getGeoJson() {
    return api.get(
      "/cameras/geojson",
    );
  },
};