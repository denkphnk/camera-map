import { useMemo, useState } from "react";

import {
  Badge,
  Button,
  Center,
  Group,
  Loader,
  Paper,
  ScrollArea,
  Select,
  Stack,
  Table,
  Text,
  TextInput,
  Title,
} from "@mantine/core";

import { useAnalyses } from "../../hooks/useAnalyses";

export function AnalysisPage() {
  const [status, setStatus] =
    useState<string | null>(
      null,
    );

  const [videoSearch, setVideoSearch] =
    useState("");

  const [
    cameraSearch,
    setCameraSearch,
  ] = useState("");

  const [
    createdFrom,
    setCreatedFrom,
  ] = useState("");

  const [createdTo, setCreatedTo] =
    useState("");

  const {
    data,
    isLoading,
    isError,
  } = useAnalyses({
    status:
      status ?? undefined,

    created_from:
      createdFrom || undefined,

    created_to:
      createdTo || undefined,
  });

  const filteredItems =
    useMemo(() => {
      return (
        data?.items.filter(
          (analysis) => {
            const videoMatch =
              !videoSearch ||
              analysis.video_name
                .toLowerCase()
                .includes(
                  videoSearch.toLowerCase(),
                );

            const cameraMatch =
              !cameraSearch ||
              analysis.camera_name
                .toLowerCase()
                .includes(
                  cameraSearch.toLowerCase(),
                );

            return (
              videoMatch &&
              cameraMatch
            );
          },
        ) ?? []
      );
    }, [
      data,
      videoSearch,
      cameraSearch,
    ]);

  function getColor(
    status: string,
  ) {
    switch (status) {
      case "done":
        return "green";

      case "processing":
        return "yellow";

      case "error":
        return "red";

      case "queued":
        return "blue";

      default:
        return "gray";
    }
  }

  function getStatusLabel(
    status: string,
  ) {
    switch (status) {
      case "queued":
        return "В очереди";

      case "processing":
        return "В обработке";

      case "done":
        return "Завершено";

      case "error":
        return "Ошибка";

      default:
        return status;
    }
  }

  function resetFilters() {
    setStatus(null);
    setVideoSearch("");
    setCameraSearch("");
    setCreatedFrom("");
    setCreatedTo("");
  }

  if (isLoading) {
    return (
      <Center py="xl">
        <Loader />
      </Center>
    );
  }

  if (isError) {
    return (
      <Center py="xl">
        <Text c="red">
          Ошибка загрузки аналитики
        </Text>
      </Center>
    );
  }

  return (
    <Stack p="lg">
      <Title order={2}>
        Аналитика
      </Title>

      <Paper
        withBorder
        radius="md"
        p="md"
      >
        <Stack>
          <Select
            label="Статус"
            placeholder="Все"
            value={status}
            onChange={setStatus}
            clearable
            data={[
              {
                value: "queued",
                label:
                  "В очереди",
              },
              {
                value:
                  "processing",
                label:
                  "В обработке",
              },
              {
                value: "done",
                label:
                  "Завершено",
              },
              {
                value: "error",
                label:
                  "Ошибка",
              },
            ]}
          />

          <Group grow>
            <TextInput
              label="Видео"
              placeholder="Поиск видео"
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
            />

            <TextInput
              label="Камера"
              placeholder="Поиск камеры"
              value={
                cameraSearch
              }
              onChange={(
                event,
              ) =>
                setCameraSearch(
                  event
                    .currentTarget
                    .value,
                )
              }
            />
          </Group>

          <Group grow>
            <TextInput
              label="Дата от"
              type="date"
              value={
                createdFrom
              }
              onChange={(
                event,
              ) =>
                setCreatedFrom(
                  event
                    .currentTarget
                    .value,
                )
              }
            />

            <TextInput
              label="Дата до"
              type="date"
              value={
                createdTo
              }
              onChange={(
                event,
              ) =>
                setCreatedTo(
                  event
                    .currentTarget
                    .value,
                )
              }
            />
          </Group>

          <Button
            variant="light"
            onClick={
              resetFilters
            }
          >
            Сбросить фильтры
          </Button>
        </Stack>
      </Paper>

      <Paper
        withBorder
        radius="md"
      >
        <ScrollArea>
          <Table>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>
                  Видео
                </Table.Th>

                <Table.Th>
                  Камера
                </Table.Th>

                <Table.Th>
                  Статус
                </Table.Th>

                <Table.Th>
                  Объекты
                </Table.Th>

                <Table.Th>
                  Ошибка
                </Table.Th>

                <Table.Th>
                  Создано
                </Table.Th>

                <Table.Th>
                  Завершено
                </Table.Th>
              </Table.Tr>
            </Table.Thead>

            <Table.Tbody>
              {filteredItems.map(
                (
                  analysis,
                ) => (
                  <Table.Tr
                    key={
                      analysis.id
                    }
                  >
                    <Table.Td>
                      {
                        analysis.video_name
                      }
                    </Table.Td>

                    <Table.Td>
                      {
                        analysis.camera_name
                      }
                    </Table.Td>

                    <Table.Td>
                      <Badge
                        color={getColor(
                          analysis.status,
                        )}
                      >
                        {getStatusLabel(
                          analysis.status,
                        )}
                      </Badge>
                    </Table.Td>

                    <Table.Td>
                      {
                        (
                          analysis.result as {
                            objects_count?: number;
                          } | null
                        )
                          ?.objects_count ??
                          0
                      }
                    </Table.Td>

                    <Table.Td>
                      {analysis.error_message ??
                        "-"}
                    </Table.Td>

                    <Table.Td>
                      {new Date(
                        analysis.created_at,
                      ).toLocaleString()}
                    </Table.Td>

                    <Table.Td>
                      {analysis.finished_at
                        ? new Date(
                            analysis.finished_at,
                          ).toLocaleString()
                        : "-"}
                    </Table.Td>
                  </Table.Tr>
                ),
              )}
            </Table.Tbody>
          </Table>
        </ScrollArea>
      </Paper>
    </Stack>
  );
}