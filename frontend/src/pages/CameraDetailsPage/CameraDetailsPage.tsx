import {
  Badge,
  Card,
  Center,
  Container,
  Group,
  Loader,
  Paper,
  SimpleGrid,
  Stack,
  Text,
  Title,
} from "@mantine/core";

import { useParams } from "react-router-dom";

import { useCameraDetails } from "../../hooks/useCameraDetails";
import type { Video } from "../../types/video.types";

const API_URL =
  import.meta.env.VITE_API_URL;

export function CameraDetailsPage() {
  const { cameraId } =
    useParams();

  const {
    data,
    isLoading,
    isError,
  } = useCameraDetails(
    cameraId ?? "",
  );

  if (isLoading) {
    return (
      <Center py="xl">
        <Loader />
      </Center>
    );
  }

  if (isError || !data) {
    return (
      <Center py="xl">
        <Text c="red">
          Ошибка загрузки камеры
        </Text>
      </Center>
    );
  }

  const camera =
    data.camera;

  return (
    <Container
      size="xl"
      py="xl"
    >
      <Stack gap="xl">
        <Paper
          withBorder
          p="lg"
          radius="lg"
        >
          <Stack gap="xs">
            <Title order={2}>
              {
                camera.camera_name
              }
            </Title>

            <Text c="dimmed">
              ID:{" "}
              {
                camera.camera_id
              }
            </Text>

            <Text>
              Адрес:{" "}
              {
                camera.camera_place
              }
            </Text>

            <Group>
              <Badge>
                Модель:{" "}
                {camera.model}
              </Badge>

              <Badge>
                Тип:{" "}
                {
                  camera.camera_type
                }
              </Badge>

              <Badge>
                Класс:{" "}
                {
                  camera.camera_class
                }
              </Badge>
            </Group>

            <Text fw={700}>
              Видео:{" "}
              {data.total}
            </Text>
          </Stack>
        </Paper>

        <Paper
          withBorder
          p="lg"
          radius="lg"
        >
          <Stack>
            <Title order={3}>
              Видео камеры
            </Title>

            {data.videos
              .length === 0 && (
              <Text c="dimmed">
                Видео отсутствуют
              </Text>
            )}

            <SimpleGrid
              cols={{
                base: 1,
                sm: 2,
                lg: 3,
              }}
            >
              {data.videos.map(
                (
                  video: any,
                ) => (
                  <Card
                    key={
                      video.id
                    }
                    withBorder
                    radius="md"
                    shadow="xs"
                    style={{
                      cursor:
                        "pointer",
                    }}
                    onClick={() =>
                      window.open(
                        `${API_URL}/videos/${video.id}/stream`,
                        "_blank",
                      )
                    }
                  >
                    <img
                      src={`${API_URL}/videos/${video.id}/preview`}
                      alt={
                        video.name
                      }
                      style={{
                        width:
                          "100%",
                        height: 180,
                        objectFit:
                          "cover",
                        borderRadius: 8,
                      }}
                    />

                    <Stack
                      mt="md"
                      gap={4}
                    >
                      <Text fw={600}>
                        {
                          video.name
                        }
                      </Text>

                      <Text
                        size="sm"
                        c="dimmed"
                      >
                        {
                          video.video_resolution
                        }
                      </Text>

                      <Text
                        size="xs"
                        c="dimmed"
                      >
                        {Math.round(
                          video.duration,
                        )}{" "}
                        сек
                      </Text>

                      <Group justify="space-between">
                        <Badge
                          color={
                            video.tracing ===
                            "Done"
                              ? "green"
                              : "yellow"
                          }
                          variant="light"
                        >
                          {
                            video.tracing
                          }
                        </Badge>

                        <Text
                          size="xs"
                          c="dimmed"
                        >
                          {new Date(
                            video.created_at,
                          ).toLocaleDateString()}
                        </Text>
                      </Group>
                    </Stack>
                  </Card>
                ),
              )}
            </SimpleGrid>
          </Stack>
        </Paper>
      </Stack>
    </Container>
  );
}