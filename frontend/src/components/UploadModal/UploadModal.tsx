import { useRef, useState } from "react";

import {
  Button,
  Group,
  Modal,
  Progress,
  Stack,
  Text,
} from "@mantine/core";

import classes from "./UploadModal.module.css";

interface UploadModalProps {
  opened: boolean;
  onClose: () => void;
}

export function UploadModal({
  opened,
  onClose,
}: UploadModalProps) {
  const inputRef =
    useRef<HTMLInputElement>(null);

  const [file, setFile] =
    useState<File | null>(null);

  const [progress] =
    useState<number>(60);

  const [isUploading] =
    useState(false);

  const [isError] =
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
  };

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title="Импорт видео"
      centered
      size="lg"
    >
      {!file && (
        <Stack>
          <div
            className={classes.dropzone}
            onClick={() =>
              inputRef.current?.click()
            }
          >
            <Text>
              Перенесите файл в данную область
            </Text>

            <Text c="dimmed">
              или загрузите из каталога вручную
            </Text>
          </div>

          <input
            ref={inputRef}
            type="file"
            accept=".mp4"
            hidden
            onChange={handleFileSelect}
          />

          <Group justify="flex-end">
            <Button
              variant="default"
              onClick={onClose}
            >
              Отмена
            </Button>

            <Button
              onClick={() =>
                inputRef.current?.click()
              }
            >
              Загрузить
            </Button>
          </Group>
        </Stack>
      )}

      {file && (
        <Stack>
          <Text fw={500}>
            {file.name}
          </Text>

          <Progress value={progress} />

          <Text size="sm">
            {progress}%
          </Text>

          {isUploading && (
            <Text c="blue">
              Идет загрузка
            </Text>
          )}

          {isError && (
            <Text c="red">
              Ошибка загрузки
            </Text>
          )}

          <Group justify="space-between">
            <Button
              variant="default"
              onClick={onClose}
            >
              Отмена
            </Button>

            <Button>
              Построить трассы
            </Button>
          </Group>
        </Stack>
      )}
    </Modal>
  );
}