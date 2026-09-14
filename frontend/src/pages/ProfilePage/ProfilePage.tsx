import { useMemo, useState } from "react";

import {
  ActionIcon,
  Avatar,
  Badge,
  Card,
  Center,
  Container,
  Group,
  Loader,
  Paper,
  ScrollArea,
  SimpleGrid,
  Stack,
  Text,
  TextInput,
  Title,
} from "@mantine/core";

import {
  IconSearch,
  IconTrash,
} from "@tabler/icons-react";

import {
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

import { videoApi } from "../../api/video.api";
import { useMe } from "../../hooks/useMe";

const API_URL =
  import.meta.env.VITE_API_URL;

export function ProfilePage() {
  const [search, setSearch] =
    useState("");

  const {
    data: me,
    isLoading,
    isError,
  } = useMe();

  const queryClient =
    useQueryClient();

  const deleteMutation =
    useMutation({
      mutationFn: (
        videoId: string,
      ) =>
        videoApi.deleteVideo(
          videoId,
        ),

      onSuccess: () => {
        queryClient.invalidateQueries(
          {
            queryKey: ["me"],
          },
        );
      },
    });

  const filteredVideos =
    useMemo(() => {
      if (!me?.videos) {
        return [];
      }

      if (!search.trim()) {
        return me.videos;
      }

      return me.videos.filter(
        (video) =>
          video.name
            .toLowerCase()
            .includes(
              search.toLowerCase(),
            ),
      );
    }, [me, search]);

  return (
    <Container
      size="xl"
      py="xl"
    >
      <Stack gap="xl">
        <Paper
          withBorder
          radius="lg"
          p="lg"
        >
          <Group>
            <Avatar
              size={72}
              radius="xl"
              color="violet"
            >
              {me?.full_name?.[0] ??
                "?"}
            </Avatar>

            <Stack gap={2}>
              <Title order={3}>
                {me?.full_name}
              </Title>

              <Text c="dimmed">
                {me?.email}
              </Text>

              <Text c="dimmed">
                Видео:{" "}
                {me?.total_videos ??
                  0}
              </Text>
            </Stack>
          </Group>
        </Paper>

        <Paper
          withBorder
          radius="lg"
          p="lg"
        >
          <Stack>
            <Title order={4}>
              Загруженные видео
            </Title>

            <TextInput
              value={search}
              onChange={(event) =>
                setSearch(
                  event.currentTarget.value,
                )
              }
              placeholder="Поиск видео"
              leftSection={
                <IconSearch size={16} />
              }
            />

            {isLoading && (
              <Center py="xl">
                <Loader />
              </Center>
            )}

            {isError && (
              <Text c="red">
                Ошибка загрузки профиля
              </Text>
            )}

            {!isLoading &&
              me && (
                <ScrollArea h={650}>
                  <SimpleGrid
                    cols={{
                      base: 1,
                      sm: 2,
                      lg: 3,
                    }}
                  >
                    {filteredVideos.map(
                      (video) => (
                        <Card
                          key={video.id}
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

                              <ActionIcon
                                color="red"
                                variant="light"
                                loading={
                                  deleteMutation.isPending
                                }
                                onClick={(
                                  event,
                                ) => {
                                  event.stopPropagation();

                                  if (
                                    confirm(
                                      "Удалить видео?",
                                    )
                                  ) {
                                    deleteMutation.mutate(
                                      video.id,
                                    );
                                  }
                                }}
                              >
                                <IconTrash size={16} />
                              </ActionIcon>
                            </Group>

                            <Text
                              size="xs"
                              c="dimmed"
                            >
                              {new Date(
                                video.created_at,
                              ).toLocaleDateString()}
                            </Text>
                          </Stack>
                        </Card>
                      ),
                    )}
                  </SimpleGrid>

                  {filteredVideos.length ===
                    0 && (
                    <Center py="xl">
                      <Text c="dimmed">
                        Видео не найдены
                      </Text>
                    </Center>
                  )}
                </ScrollArea>
              )}
          </Stack>
        </Paper>
      </Stack>
    </Container>
  );
}