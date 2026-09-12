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
} from "@tabler/icons-react";

import {
  NavLink,
  useLocation,
  useNavigate,
} from "react-router-dom";

import { useAuth } from "../../context/AuthContext";

import classes from "./Sidebar.module.css";

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
    <Box className={classes.sidebar}>
      <Stack gap="xs">
        <Tooltip
          label="Карта"
          position="right"
        >
          <ActionIcon
            component={NavLink}
            to="/map"
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
          <br />
        <Tooltip
          label="Видео"
          position="right"
        >
          <ActionIcon
            component={NavLink}
            to="/profile"
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
      </Stack>

      <Box className={classes.bottom}>
        <Divider mb="md" />

        <Stack gap="xs">
          <Tooltip
            label="Профиль"
            position="right"
          >
            <ActionIcon
              component={NavLink}
              to="/profile"
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