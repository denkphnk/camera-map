import { api } from "./axios";

export const videoApi = {
  upload(formData: FormData) {
    return api.post(
      "/videos/upload",
      formData,
    );
  },
};