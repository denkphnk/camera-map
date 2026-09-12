import { Outlet } from "react-router-dom";

import { Sidebar } from "./Sidebar";

import classes from "./AppShellLayout.module.css";

export function AppShellLayout() {
  return (
    <div className={classes.layout}>
      <Sidebar />

      <main className={classes.content}>
        <Outlet />
      </main>
    </div>
  );
}