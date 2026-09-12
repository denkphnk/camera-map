let accessToken: string | null = null;

export const authService = {
  setToken(token: string) {
    accessToken = token;
  },

  getToken() {
    return accessToken;
  },

  clearToken() {
    accessToken = null;
  },
};