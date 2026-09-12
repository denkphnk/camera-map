export interface GeoJsonFeature {
  type: string;

  properties: {
    camera_id: string;
    has_video: boolean;
  };

  geometry: {
    type: string;

    coordinates: [
      number,
      number,
    ];
  };
}

export interface GeoJsonResponse {
  type: string;

  features: GeoJsonFeature[];
}