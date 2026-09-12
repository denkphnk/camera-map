import { api } from "./axios";

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  full_name: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
}

export async function login(
  payload: LoginRequest,
) {
  const { data } =
    await api.post<TokenResponse>(
      "/auth/login",
      payload,
    );

  return data;
}

export async function register(
  payload: RegisterRequest,
) {
  const { data } = await api.post(
    "/auth/register",
    payload,
  );

  return data;
}

export async function refresh(
  refreshToken: string,
) {
  const { data } =
    await api.post<TokenResponse>(
      "/auth/refresh",
      {
        refresh_token:
          refreshToken,
      },
    );

  return data;
}

export async function logout(
  refreshToken: string,
) {
  await api.post("/auth/logout", {
    refresh_token:
      refreshToken,
  });
}