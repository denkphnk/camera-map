import classes from "./CameraMarker.module.css";

interface CameraMarkerProps {
  hasVideo: boolean;
}

export function CameraMarker({
  hasVideo,
}: CameraMarkerProps) {
  return (
    <div
      className={
        hasVideo
          ? classes.active
          : classes.default
      }
    />
  );
}