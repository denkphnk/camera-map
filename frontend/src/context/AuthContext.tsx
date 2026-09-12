import {
  createContext,
  useContext,
  useState,
} from "react";

import { tokenService } from "../services/token.service";

interface AuthContextType {
  isAuthenticated: boolean;

  login: (
    accessToken: string,
    refreshToken: string,
  ) => void;

  logout: () => void;
}

const AuthContext =
  createContext<AuthContextType | null>(
    null,
  );

export function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [
    isAuthenticated,
    setIsAuthenticated,
  ] = useState(
    !!tokenService.getAccessToken(),
  );

  function handleLogin(
    accessToken: string,
    refreshToken: string,
  ) {
    tokenService.setTokens(
      accessToken,
      refreshToken,
    );

    setIsAuthenticated(true);
  }

  function handleLogout() {
    tokenService.clear();

    setIsAuthenticated(false);
  }

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        login: handleLogin,
        logout: handleLogout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context =
    useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used inside AuthProvider",
    );
  }

  return context;
}