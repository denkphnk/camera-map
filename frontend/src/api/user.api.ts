import { api } from "./axios";

export const userApi = {
  getMe() {
    return api.get("/users/me");
  },
};