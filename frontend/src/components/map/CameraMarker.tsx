import {
  Indicator,
  ThemeIcon,
} from "@mantine/core";

import {
  IconVideo,
} from "@tabler/icons-react";

interface CameraMarkerProps {
  hasVideo: boolean;
}

export function CameraMarker({
  hasVideo,
}: CameraMarkerProps) {
  return (
    <Indicator
      disabled={!hasVideo}
      color="green"
      size={10}
      offset={2}
    >
      <ThemeIcon
        radius="xl"
        size="lg"
        color="violet"
        variant="filled"
      >
        <IconVideo size={14} />
      </ThemeIcon>
    </Indicator>
  );
}