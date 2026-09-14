import { useQuery } from "@tanstack/react-query";

import { userApi } from "../api/user.api";

import type { MeResponse } from "../types/user.types";

export function useMe() {
  return useQuery<MeResponse>({
    queryKey: ["me"],

    queryFn: async () => {
      const response =
        await userApi.getMe();

      return response.data;
    },
  });
}