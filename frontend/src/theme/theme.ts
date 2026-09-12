import { createTheme } from "@mantine/core";

export const theme = createTheme({
  primaryColor: "violet",

  defaultRadius: "md",

  fontFamily:
    "Inter, ui-sans-serif, system-ui, sans-serif",

  colors: {
    violet: [
      "#F5F3FF",
      "#EDE9FE",
      "#DDD6FE",
      "#C4B5FD",
      "#A78BFA",
      "#8B5CF6",
      "#7C3AED",
      "#6D28D9",
      "#5B21B6",
      "#4C1D95",
    ],
  },

  radius: {
    xs: "6px",
    sm: "8px",
    md: "12px",
    lg: "16px",
    xl: "20px",
  },

  shadows: {
    xs: "0 1px 2px rgba(0,0,0,0.05)",
    sm: "0 2px 6px rgba(0,0,0,0.08)",
    md: "0 4px 12px rgba(0,0,0,0.08)",
    lg: "0 10px 24px rgba(0,0,0,0.10)",
  },
});