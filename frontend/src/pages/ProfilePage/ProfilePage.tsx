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
  Tabs,
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
import { useAllVideos } from "../../hooks/useAllVideos";

import type { Video } from "../../types/video.types";
import type { UserVideo } from "../../types/user.types";

const API_URL =
  import.meta.env.VITE_API_URL;

export function ProfilePage() {
  const [videoSearch, setVideoSearch] =
    useState("");

  const [
    authorSearch,
    setAuthorSearch,
  ] = useState("");

  const {
    data: me,
    isLoading,
    isError,
  } = useMe();

  const {
    data: allVideos,
    isLoading: allVideosLoading,
  } = useAllVideos();

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

        queryClient.invalidateQueries(
          {
            queryKey: ["videos"],
          },
        );
      },
    });

  const filteredMyVideos =
    useMemo(() => {
      if (!me?.videos) {
        return [];
      }

      if (!videoSearch.trim()) {
        return me.videos;
      }

      return me.videos.filter(
        (video) =>
          video.name
            .toLowerCase()
            .includes(
              videoSearch.toLowerCase(),
            ),
      );
    }, [me, videoSearch]);

  const filteredAllVideos =
    useMemo(() => {
      if (!allVideos?.items) {
        return [];
      }

      return allVideos.items.filter(
        (video) => {
          const nameMatch =
            !videoSearch ||
            video.name
              .toLowerCase()
              .includes(
                videoSearch.toLowerCase(),
              );

          const authorMatch =
            !authorSearch ||
            (
              video.author_name ??
              ""
            )
              .toLowerCase()
              .includes(
                authorSearch.toLowerCase(),
              );

          return (
            nameMatch &&
            authorMatch
          );
        },
      );
    }, [
      allVideos,
      videoSearch,
      authorSearch,
    ]);

  function renderVideoCard(
    video: Video | UserVideo,
    showDelete = false,
  ) {
    return (
      <Card
        key={video.id}
        withBorder
        radius="md"
        shadow="xs"
        style={{
          cursor: "pointer",
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
          alt={video.name}
          style={{
            width: "100%",
            height: 180,
            objectFit: "cover",
            borderRadius: 8,
          }}
        />

        <Stack
          mt="md"
          gap={4}
        >
          <Text fw={600}>
            {video.name}
          </Text>

          {"author_name" in video && (
            <Text
              size="sm"
              c="dimmed"
            >
              Автор:{" "}
              {video.author_name}
            </Text>
          )}

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
                "ready"
                  ? "green"
                  : "yellow"
              }
              variant="light"
            >
              {video.tracing}
            </Badge>

            {showDelete && (
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
            )}
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
    );
  }

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
          <Tabs
            defaultValue="my"
          >
            <Tabs.List>
              <Tabs.Tab value="my">
                Мои видео
              </Tabs.Tab>

              <Tabs.Tab value="all">
                Все видео
              </Tabs.Tab>
            </Tabs.List>

            <Tabs.Panel
              value="my"
              pt="md"
            >
              <Stack>
                <TextInput
                  value={videoSearch}
                  onChange={(
                    event,
                  ) =>
                    setVideoSearch(
                      event
                        .currentTarget
                        .value,
                    )
                  }
                  placeholder="Поиск видео"
                  leftSection={
                    <IconSearch
                      size={16}
                    />
                  }
                />

                {isLoading && (
                  <Center py="xl">
                    <Loader />
                  </Center>
                )}

                {isError && (
                  <Text c="red">
                    Ошибка загрузки
                    профиля
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
                        {filteredMyVideos.map(
                          (
                            video,
                          ) =>
                            renderVideoCard(
                              video,
                              true,
                            ),
                        )}
                      </SimpleGrid>
                    </ScrollArea>
                  )}
              </Stack>
            </Tabs.Panel>

            <Tabs.Panel
              value="all"
              pt="md"
            >
              <Stack>
                <TextInput
                  value={videoSearch}
                  onChange={(
                    event,
                  ) =>
                    setVideoSearch(
                      event
                        .currentTarget
                        .value,
                    )
                  }
                  placeholder="Поиск по названию"
                  leftSection={
                    <IconSearch
                      size={16}
                    />
                  }
                />

                <TextInput
                  value={
                    authorSearch
                  }
                  onChange={(
                    event,
                  ) =>
                    setAuthorSearch(
                      event
                        .currentTarget
                        .value,
                    )
                  }
                  placeholder="Поиск по пользователю"
                />

                {allVideosLoading && (
                  <Center py="xl">
                    <Loader />
                  </Center>
                )}

                {!allVideosLoading && (
                  <ScrollArea h={650}>
                    <SimpleGrid
                      cols={{
                        base: 1,
                        sm: 2,
                        lg: 3,
                      }}
                    >
                      {filteredAllVideos.map(
                        (
                          video,
                        ) =>
                          renderVideoCard(
                            video,
                          ),
                      )}
                    </SimpleGrid>
                  </ScrollArea>
                )}
              </Stack>
            </Tabs.Panel>
          </Tabs>
        </Paper>
      </Stack>
    </Container>
  );
}