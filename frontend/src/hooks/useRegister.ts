import { useMutation } from "@tanstack/react-query";

import { register } from "../api/auth.api";

export function useRegister() {
  return useMutation({
    mutationFn: register,
  });
}