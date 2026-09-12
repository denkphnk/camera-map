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
              Вход
            </Title>

            <Text c="dimmed">
              Авторизация в системе
            </Text>

            {error && (
              <Alert color="red">
                {error}
              </Alert>
            )}

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
              Войти
            </Button>

            <Text size="sm">
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