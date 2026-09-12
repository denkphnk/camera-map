import axios from "axios";

import { refresh } from "./auth.api";

import { tokenService } from "../services/token.service";

export const api = axios.create({
  baseURL:
    "http://localhost:8000",
});

api.interceptors.request.use(
  (config) => {
    const token =
      tokenService.getAccessToken();

    if (token) {
      config.headers.Authorization =
        `Bearer ${token}`;
    }

    return config;
  },
);

api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest =
      error.config;

    if (
      error.response?.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        const refreshToken =
          tokenService.getRefreshToken();

        if (!refreshToken) {
          throw error;
        }

        const tokens =
          await refresh(
            refreshToken,
          );

        tokenService.setTokens(
          tokens.access_token,
          tokens.refresh_token,
        );

        originalRequest.headers.Authorization =
          `Bearer ${tokens.access_token}`;

        return api(
          originalRequest,
        );
      } catch {
        tokenService.clear();

        window.location.href =
          "/login";
      }
    }

    return Promise.reject(error);
  },
);