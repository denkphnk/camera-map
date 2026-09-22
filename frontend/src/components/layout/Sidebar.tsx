import {
  ActionIcon,
  Box,
  Divider,
  Stack,
  Tooltip,
} from "@mantine/core";

import {
  IconLogout,
  IconMap2,
  IconUser,
  IconVideo,
  IconChartBar,
} from "@tabler/icons-react";

import {
  NavLink,
  useLocation,
  useNavigate,
} from "react-router-dom";

import { useAuth } from "../../context/AuthContext";

export function Sidebar() {
  const location = useLocation();

  const navigate = useNavigate();

  const auth = useAuth();

  const isActive = (
    path: string,
  ) =>
    location.pathname.startsWith(
      path,
    );

  function handleLogout() {
    auth.logout();

    navigate("/login");
  }

  return (
    <Box
      w={56}
      h="100vh"
      p={8}
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent:
          "space-between",
        borderRight:
          "1px solid var(--mantine-color-dark-4)",
      }}
    >
      <Stack gap="xs">
        <Tooltip
          label="Карта"
          position="right"
        >
          <ActionIcon
            component={NavLink}
            to="/map"
            color="violet"
            variant={
              isActive("/map")
                ? "filled"
                : "subtle"
            }
            size={40}
            radius="md"
          >
            <IconMap2 size={20} />
          </ActionIcon>
        </Tooltip>

        <Tooltip
          label="Видео"
          position="right"
        >
          <ActionIcon
            component={NavLink}
            to="/profile"
            color="violet"
            variant={
              isActive("/profile")
                ? "filled"
                : "subtle"
            }
            size={40}
            radius="md"
          >
            <IconVideo size={20} />
          </ActionIcon>
        </Tooltip>

        <Tooltip
          label="Аналитика"
          position="right"
        >
          <ActionIcon
            component={NavLink}
            to="/analysis"
            color="violet"
            variant={
              isActive("/analysis")
                ? "filled"
                : "subtle"
            }
            size={40}
            radius="md"
          >
            <IconChartBar size={20} />
          </ActionIcon>
        </Tooltip>
      </Stack>

      <Box>
        <Divider mb="md" />

        <Stack gap="xs">
          <Tooltip
            label="Профиль"
            position="right"
          >
            <ActionIcon
              component={NavLink}
              to="/profile"
              color="violet"
              variant={
                isActive("/profile")
                  ? "filled"
                  : "subtle"
              }
              size={40}
              radius="md"
            >
              <IconUser size={20} />
            </ActionIcon>
          </Tooltip>

          <Tooltip
            label="Выход"
            position="right"
          >
            <ActionIcon
              variant="subtle"
              size={40}
              radius="md"
              color="gray"
              onClick={
                handleLogout
              }
            >
              <IconLogout size={20} />
            </ActionIcon>
          </Tooltip>
        </Stack>
      </Box>
    </Box>
  );
}