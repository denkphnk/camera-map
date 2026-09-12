import { Card, Group, Text } from "@mantine/core";

import classes from "./CameraCard.module.css";

interface CameraCardProps {
  id: string;
  address: string;
  latitude: number;
  longitude: number;
  camerasCount: number;
}

export function CameraCard({
  id,
  address,
  latitude,
  longitude,
  camerasCount,
}: CameraCardProps) {
  return (
    <Card
      className={classes.card}
      radius="md"
      withBorder
    >
      <Text fw={600}>
        Комплекс камер #{id}
      </Text>

      <Text
        size="sm"
        c="dimmed"
      >
        {address}
      </Text>

      <Text
        size="xs"
        c="dimmed"
      >
        {longitude}, {latitude}
      </Text>

      <Group justify="space-between">
        <Text size="sm">
          Кол-во камер: {camerasCount}
        </Text>
      </Group>
    </Card>
  );
}