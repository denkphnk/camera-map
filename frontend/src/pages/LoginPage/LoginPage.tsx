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

import { useAuth } from "../../context/AuthContext";
import { useLogin } from "../../hooks/useLogin";

import classes from "./LoginPage.module.css";

export function LoginPage() {
  const navigate = useNavigate();

  const auth = useAuth();

  const { mutateAsync, isPending } =
    useLogin();

  const [email, setEmail] =
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
      const result =
        await mutateAsync({
          email,
          password,
        });

      auth.login(
        result.access_token,
        result.refresh_token,
      );

      navigate("/map");
    } catch {
      setError(
        "Неверный email или пароль",
      );
    }
  }

  return (
    <div className={classes.page}>
      <div
        className={classes.background}
      />

      <Paper
        className={classes.card}
        radius="xl"
        p="xl"
        withBorder
        bg="dark.7"
      >
        <form
          onSubmit={handleSubmit}
        >
          <Stack>
            <Title
              order={2}
              ta="center"
              c="white"
            >
              Вход в систему
            </Title>

            <Text
              ta="center"
              c="dimmed"
              size="sm"
            >
              Карта камер и видео
            </Text>

            {error && (
              <Alert color="red">
                {error}
              </Alert>
            )}

            <TextInput
              label="Email"
              placeholder="example@mail.com"
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
              placeholder="Введите пароль"
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
              color="violet"
              loading={isPending}
              fullWidth
            >
              Войти
            </Button>

            <Text
              size="sm"
              ta="center"
            >
              Нет аккаунта?{" "}
              <Anchor
                component={Link}
                to="/register"
              >
                Зарегистрироваться
              </Anchor>
            </Text>
          </Stack>
        </form>
      </Paper>
    </div>
  );
}