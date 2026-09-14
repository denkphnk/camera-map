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
            Создание нового аккаунта
          </Text>

            {error && (
              <Alert color="red">
                {error}
              </Alert>
            )}

            <TextInput
              label="ФИО"
              placeholder="Иванов Иван Иванович"
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
              placeholder="Придумайте пароль"
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
              Зарегистрироваться
            </Button>

            <Text
              size="sm"
              ta="center"
            >
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