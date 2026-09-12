import {
  Avatar,
  Badge,
  Card,
  Group,
  ScrollArea,
  SimpleGrid,
  Stack,
  Text,
  TextInput,
  Title,
} from "@mantine/core";

import { IconSearch } from "@tabler/icons-react";

import classes from "./ProfilePage.module.css";

export function ProfilePage() {
  return (
    <div className={classes.page}>
      <div className={classes.content}>
        <Card
          withBorder
          radius="lg"
          className={classes.userCard}
        >
          <Group>
            <Avatar
              size={72}
              radius="xl"
            >
              ИИ
            </Avatar>

            <Stack gap={4}>
              <Title order={3}>
                Иван Иванов
              </Title>

              <Text c="dimmed">
                ivan@mail.ru
              </Text>

              <Text c="dimmed">
                ООО Камеры России
              </Text>
            </Stack>
          </Group>
        </Card>

        <Card
          withBorder
          radius="lg"
        >
          <Stack>
            <Title order={4}>
              Последние видео
            </Title>

            <TextInput
              placeholder="Поиск по названию или пользователю"
              leftSection={
                <IconSearch size={16} />
              }
            />

            <ScrollArea h={600}>
              <SimpleGrid cols={2}>
                {Array.from({
                  length: 10,
                }).map((_, index) => (
                  <Card
                    key={index}
                    withBorder
                    radius="md"
                  >
                    <div
                      className={
                        classes.preview
                      }
                    />

                    <Stack
                      mt="sm"
                      gap={4}
                    >
                      <Text fw={600}>
                        Видео №
                        {index + 1}
                      </Text>

                      <Text
                        size="sm"
                        c="dimmed"
                      >
                        Камера #123456
                      </Text>

                      <Group
                        justify="space-between"
                      >
                        <Badge
                          color="green"
                        >
                          Обработано
                        </Badge>

                        <Text
                          size="xs"
                          c="dimmed"
                        >
                          12.09.2026
                        </Text>
                      </Group>
                    </Stack>
                  </Card>
                ))}
              </SimpleGrid>
            </ScrollArea>
          </Stack>
        </Card>
      </div>
    </div>
  );
}