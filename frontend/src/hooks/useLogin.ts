import { useMutation } from "@tanstack/react-query";

import { login } from "../api/auth.api";

export function useLogin() {
  return useMutation({
    mutationFn: login,
  });
}