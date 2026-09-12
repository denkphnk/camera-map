import {
  Badge,
  Button,
  Card,
  Group,
  ScrollArea,
  Stack,
  Tabs,
  Text,
  TextInput,
  Title,
} from "@mantine/core";

import { IconSearch } from "@tabler/icons-react";

import classes from "./LocationPage.module.css";

export function LocationPage() {
  return (
    <div className={classes.page}>
      <Card
        withBorder
        radius="lg"
        mb="md"
      >
        <Stack gap={4}>
          <Title order={3}>
            Комплекс камер #123456
          </Title>

          <Text c="dimmed">
            Красногвардейский 1-й проезд
          </Text>

          <Text c="dimmed">
            55.123456, 37.123456
          </Text>
        </Stack>
      </Card>

      <Tabs
        defaultValue="videos"
        variant="outline"
      >
        <Tabs.List>
          <Tabs.Tab value="videos">
            Видео
          </Tabs.Tab>

          <Tabs.Tab value="analytics">
            Анализы
          </Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel
          value="videos"
          pt="md"
        >
          <Card
            withBorder
            radius="lg"
          >
            <Stack>
              <Group
                justify="space-between"
              >
                <Title order={4}>
                  Видео
                </Title>

                <Button>
                  Импорт видео
                </Button>
              </Group>

              <TextInput
                placeholder="Поиск видео"
                leftSection={
                  <IconSearch size={16} />
                }
              />

              <ScrollArea h={600}>
                <Stack>
                  {Array.from({
                    length: 8,
                  }).map((_, index) => (
                    <Card
                      key={index}
                      withBorder
                    >
                      <Group
                        justify="space-between"
                      >
                        <div>
                          <Text fw={600}>
                            Видео №
                            {index + 1}
                          </Text>

                          <Text
                            size="sm"
                            c="dimmed"
                          >
                            Автор:
                            Иван Иванов
                          </Text>
                        </div>

                        <Badge color="green">
                          Обработано
                        </Badge>
                      </Group>
                    </Card>
                  ))}
                </Stack>
              </ScrollArea>
            </Stack>
          </Card>
        </Tabs.Panel>

        <Tabs.Panel
          value="analytics"
          pt="md"
        >
          <Card
            withBorder
            radius="lg"
          >
            <Stack>
              <Title order={4}>
                Анализы
              </Title>

              <TextInput
                placeholder="Поиск анализа"
                leftSection={
                  <IconSearch size={16} />
                }
              />

              <ScrollArea h={600}>
                <Stack>
                  {Array.from({
                    length: 5,
                  }).map((_, index) => (
                    <Card
                      key={index}
                      withBorder
                    >
                      <Group
                        justify="space-between"
                      >
                        <div>
                          <Text fw={600}>
                            Анализ №
                            {index + 1}
                          </Text>

                          <Text
                            size="sm"
                            c="dimmed"
                          >
                            Построение
                            трасс
                          </Text>
                        </div>

                        <Badge>
                          Завершен
                        </Badge>
                      </Group>
                    </Card>
                  ))}
                </Stack>
              </ScrollArea>
            </Stack>
          </Card>
        </Tabs.Panel>
      </Tabs>
    </div>
  );
}