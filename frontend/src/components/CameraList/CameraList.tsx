import { Stack } from "@mantine/core";

import { CameraCard } from "./CameraCard";

export function CameraList() {
  return (
    <Stack gap="sm">
      {Array.from({ length: 12 }).map((_, index) => (
        <CameraCard
          key={index}
          id={`12345${index}`}
          address="Красногвардейский 1-й проезд"
          latitude={55.123456}
          longitude={37.123456}
          camerasCount={4}
        />
      ))}
    </Stack>
  );
}