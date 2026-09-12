import { useState } from "react";

import {
  Alert,
  Anchor,
  Button,
  Paper,
  PasswordInput,
  Stack,
  Text,
  TextInput,
  Title,
} from "@mantine/core";

import { Link, useNavigate } from "react-router-dom";

import { useRegister } from "../../hooks/useRegister";

import classes from "./RegisterPage.module.css";

export function RegisterPage() {
  const navigate = useNavigate();

  const { mutateAsync, isPending } =
    useRegister();

  const [email, setEmail] =
    useState("");

  const [fullName, setFullName] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [error, setError] =
    useState("");

  async function handleSubmit(
    event: React.FormEvent,
  ) {
    event.preventDefault();

    setError("");

    try {
      await mutateAsync({
        email,
        full_name: fullName,
        password,
      });

      navigate("/login");
    } catch {
      setError(
        "Ошибка регистрации",
      );
    }
  }

  return (
    <div className={classes.page}>
      <Paper
        shadow="md"
        radius="lg"
        p="xl"
        w={420}
      >
        <form
          onSubmit={handleSubmit}
        >
          <Stack>
            <Title order={2}>
              Регистрация
            </Title>

            <Text c="dimmed">
              Создание аккаунта
            </Text>

            {error && (
              <Alert color="red">
                {error}
              </Alert>
            )}

            <TextInput
              label="ФИО"
              value={fullName}
              onChange={(event) =>
                setFullName(
                  event.currentTarget
                    .value,
                )
              }
              required
            />

            <TextInput
              label="Email"
              value={email}
              onChange={(event) =>
                setEmail(
                  event.currentTarget
                    .value,
                )
              }
              required
            />

            <PasswordInput
              label="Пароль"
              value={password}
              onChange={(event) =>
                setPassword(
                  event.currentTarget
                    .value,
                )
              }
              required
            />

            <Button
              type="submit"
              loading={isPending}
            >
              Зарегистрироваться
            </Button>

            <Text size="sm">
              Уже есть аккаунт?{" "}
              <Anchor
                component={Link}
                to="/login"
              >
                Войти
              </Anchor>
            </Text>
          </Stack>
        </form>
      </Paper>
    </div>
  );
}