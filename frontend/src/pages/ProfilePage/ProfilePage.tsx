import {
  Avatar,
  Badge,
  Card,
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
  Center,
} from "@mantine/core";

import { IconSearch } from "@tabler/icons-react";

import { useVideos } from "../../hooks/useVideos";

export function ProfilePage() {
  const {
    data,
    isLoading,
    isError,
  } = useVideos();

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
              ИИ
            </Avatar>

            <Stack gap={2}>
              <Title order={3}>
                Личный кабинет
              </Title>

              <Text c="dimmed">
                Мои видео
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
                Ошибка загрузки видео
              </Text>
            )}

            {!isLoading &&
              data && (
                <ScrollArea h={650}>
                  <SimpleGrid
                    cols={{
                      base: 1,
                      sm: 2,
                      lg: 3,
                    }}
                  >
                    {data.items.map(
                      (video) => (
                        <Card
                          key={video.id}
                          withBorder
                          radius="md"
                          shadow="xs"
                        >
                          <Paper
                            radius="md"
                            h={180}
                            style={{
                              background:
                                "linear-gradient(135deg,#2e2e38,#1f1f27)",
                            }}
                          />

                          <Stack
                            mt="md"
                            gap={4}
                          >
                            <Text fw={600}>
                              {video.name}
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
                              {
                                video.duration
                              }
                              s
                            </Text>

                            <Group justify="space-between">
                              <Badge
                                color="green"
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
                </ScrollArea>
              )}
          </Stack>
        </Paper>
      </Stack>
    </Container>
  );
}