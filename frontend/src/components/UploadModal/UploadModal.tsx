import { useRef, useState } from "react";

import {
  Alert,
  Button,
  Group,
  Modal,
  Paper,
  Progress,
  Stack,
  Text,
  ThemeIcon,
} from "@mantine/core";

import { notifications } from "@mantine/notifications";

import { IconUpload } from "@tabler/icons-react";

import { videoApi } from "../../api/video.api";

interface UploadModalProps {
  opened: boolean;
  onClose: () => void;
  cameraId: string;
}

export function UploadModal({
  opened,
  onClose,
  cameraId,
}: UploadModalProps) {
  const inputRef =
    useRef<HTMLInputElement>(null);

  const [file, setFile] =
    useState<File | null>(null);

  const [progress, setProgress] =
    useState(0);

  const [isUploading, setIsUploading] =
    useState(false);

  const [isError, setIsError] =
    useState(false);

  const handleFileSelect = (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const selected =
      event.target.files?.[0];

    if (!selected) {
      return;
    }

    setFile(selected);
    setProgress(0);
    setIsError(false);
  };

  async function handleUpload() {
    if (!file || !cameraId) {
      return;
    }

    try {
      setIsUploading(true);
      setIsError(false);

      setProgress(30);

      await videoApi.upload(
        file,
        cameraId,
      );

      setProgress(100);

      notifications.show({
        color: "green",
        title: "Успешно",
        message:
          "Видео успешно загружено",
      });

      setTimeout(() => {
        handleClose();
      }, 700);
    } catch {
      setIsError(true);

      notifications.show({
        color: "red",
        title: "Ошибка",
        message:
          "Не удалось загрузить видео",
      });
    } finally {
      setIsUploading(false);
    }
  }

  function handleClose() {
    setFile(null);
    setProgress(0);
    setIsError(false);
    setIsUploading(false);

    onClose();
  }

  return (
    <Modal
      opened={opened}
      onClose={handleClose}
      title="Импорт видео"
      centered
      size="lg"
    >
      {!file && (
        <Stack>
          <Paper
            withBorder
            radius="md"
            p="xl"
            style={{
              minHeight: 220,
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
            onClick={() =>
              inputRef.current?.click()
            }
          >
            <Stack
              align="center"
              gap="xs"
            >
              <ThemeIcon
                size={56}
                radius="xl"
                variant="light"
                color="violet"
              >
                <IconUpload size={28} />
              </ThemeIcon>

              <Text fw={600}>
                Выберите видео
              </Text>

              <Text
                size="sm"
                c="dimmed"
              >
                MP4 файл для загрузки
              </Text>
            </Stack>
          </Paper>

          <input
            ref={inputRef}
            type="file"
            accept=".mp4"
            hidden
            onChange={
              handleFileSelect
            }
          />

          <Group justify="flex-end">
            <Button
              variant="default"
              onClick={handleClose}
            >
              Отмена
            </Button>

            <Button
              color="violet"
              onClick={() =>
                inputRef.current?.click()
              }
            >
              Выбрать файл
            </Button>
          </Group>
        </Stack>
      )}

      {file && (
        <Stack>
          <Paper
            withBorder
            radius="md"
            p="md"
          >
            <Text fw={600}>
              {file.name}
            </Text>

            <Text
              size="sm"
              c="dimmed"
            >
              {(
                file.size /
                1024 /
                1024
              ).toFixed(2)}{" "}
              MB
            </Text>
          </Paper>

          <Progress
            value={progress}
            color="violet"
          />

          <Text
            size="sm"
            ta="center"
          >
            {progress}%
          </Text>

          {isUploading && (
            <Alert color="blue">
              Загрузка видео...
            </Alert>
          )}

          {isError && (
            <Alert color="red">
              Ошибка загрузки
            </Alert>
          )}

          <Group justify="space-between">
            <Button
              variant="default"
              onClick={handleClose}
            >
              Отмена
            </Button>

            <Button
              color="violet"
              loading={isUploading}
              onClick={
                handleUpload
              }
            >
              Загрузить
            </Button>
          </Group>
        </Stack>
      )}
    </Modal>
  );
}