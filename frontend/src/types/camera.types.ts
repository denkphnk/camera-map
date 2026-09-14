export interface GeoJsonFeature {
  type: string;

  properties: {
    camera_id: string;
    db_id: string;

    address: string;

    camera_name: string;

    model: string | null;

    camera_type: string | null;

    camera_class: string | null;

    video_count: number;

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