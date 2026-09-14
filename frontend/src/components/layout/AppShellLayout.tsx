import {
  AppShell,
} from "@mantine/core";

import {
  Outlet,
} from "react-router-dom";

import { Sidebar } from "./Sidebar";

export function AppShellLayout() {
  return (
    <AppShell
      padding={0}
      navbar={{
        width: 72,
        breakpoint: 0,
      }}
    >
      <AppShell.Navbar>
        <Sidebar />
      </AppShell.Navbar>

      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}