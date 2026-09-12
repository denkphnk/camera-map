import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

import {
  Button,
  Container,
  Paper,
  PasswordInput,
  Stack,
  Text,
  TextInput,
  Title,
} from "@mantine/core";

import { notifications } from "@mantine/notifications";

import { login } from "../../api/auth";

export function LoginPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    try {
      setLoading(true);

      const response = await login({
        email,
        password,
      });

      localStorage.setItem(
        "access_token",
        response.access_token
      );

      localStorage.setItem(
        "refresh_token",
        response.refresh_token
      );

      navigate("/map");
    } catch {
      notifications.show({
        title: "Ошибка",
        message: "Неверный логин или пароль",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container size={420} mt={120}>
      <Paper p="xl" radius="md" withBorder>
        <Stack>
          <Title order={2}>Авторизация</Title>

          <TextInput
            label="Почта"
            value={email}
            onChange={(e) =>
              setEmail(e.currentTarget.value)
            }
          />

          <PasswordInput
            label="Пароль"
            value={password}
            onChange={(e) =>
              setPassword(e.currentTarget.value)
            }
          />

          <Button
            loading={loading}
            onClick={handleLogin}
          >
            Войти
          </Button>

          <Text size="sm">
            Нет аккаунта?{" "}
            <Link to="/register">
              Зарегистрироваться
            </Link>
          </Text>
        </Stack>
      </Paper>
    </Container>
  );
}