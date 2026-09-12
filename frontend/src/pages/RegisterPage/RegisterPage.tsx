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

import { register } from "../../api/auth";

export function RegisterPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    try {
      setLoading(true);

      await register({
        email,
        full_name: fullName,
        password,
      });

      notifications.show({
        title: "Успешно",
        message: "Аккаунт создан",
      });

      navigate("/");
    } catch {
      notifications.show({
        title: "Ошибка",
        message: "Не удалось зарегистрироваться",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container size={420} mt={120}>
      <Paper p="xl" radius="md" withBorder>
        <Stack>
          <Title order={2}>Регистрация</Title>

          <TextInput
            label="ФИО"
            value={fullName}
            onChange={(e) =>
              setFullName(e.currentTarget.value)
            }
          />

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
            onClick={handleRegister}
          >
            Зарегистрироваться
          </Button>

          <Text size="sm">
            Уже есть аккаунт?{" "}
            <Link to="/">Войти</Link>
          </Text>
        </Stack>
      </Paper>
    </Container>
  );
}