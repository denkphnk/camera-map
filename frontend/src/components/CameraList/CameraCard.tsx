import {
  Badge,
  Card,
  Group,
  Stack,
  Text,
} from "@mantine/core";

interface CameraCardProps {
  id: string;
  address: string;
  latitude: number;
  longitude: number;
  camerasCount: number;
  selected?: boolean;
}

export function CameraCard({
  id,
  address,
  latitude,
  longitude,
  camerasCount,
  selected = false,
}: CameraCardProps) {
  return (
    <Card
      withBorder
      radius="lg"
      shadow={
        selected
          ? "md"
          : "xs"
      }
      p="md"
      style={{
        cursor: "pointer",
        transition: "0.15s",
        borderColor: selected
          ? "var(--mantine-color-violet-5)"
          : undefined,
      }}
    >
      <Stack gap="xs">
        <Group justify="space-between">
          <Text fw={700}>
            Камера
          </Text>

          <Badge
            color="violet"
            variant="light"
          >
            {camerasCount}
          </Badge>
        </Group>

        <Text size="sm">
          #{id}
        </Text>

        <Text
          size="xs"
          c="dimmed"
        >
          {address}
        </Text>

        <Text
          size="xs"
          c="dimmed"
        >
          {latitude.toFixed(5)},
          {" "}
          {longitude.toFixed(5)}
        </Text>
      </Stack>
    </Card>
  );
}