import {
  Navigate,
  createBrowserRouter,
} from "react-router-dom";

import { AppShellLayout } from "../components/layout/AppShellLayout";

import { ProtectedRoute } from "./ProtectedRoute";

import { LoginPage } from "../pages/LoginPage/LoginPage";
import { RegisterPage } from "../pages/RegisterPage/RegisterPage";
import { MapPage } from "../pages/MapPage/MapPage";
import { ProfilePage } from "../pages/ProfilePage/ProfilePage";
import { LocationPage } from "../pages/LocationPage/LocationPage";

export const router =
  createBrowserRouter([
    {
      path: "/",
      element: (
        <Navigate
          to="/map"
          replace
        />
      ),
    },

    {
      path: "/login",
      element: <LoginPage />,
    },

    {
      path: "/register",
      element: <RegisterPage />,
    },

    {
      element: <ProtectedRoute />,
      children: [
        {
          element: (
            <AppShellLayout />
          ),

          children: [
            {
              path: "/map",
              element: <MapPage />,
            },

            {
              path: "/profile",
              element: (
                <ProfilePage />
              ),
            },

            {
              path: "/location/:id",
              element: (
                <LocationPage />
              ),
            },
          ],
        },
      ],
    },

    {
      path: "*",
      element: (
        <Navigate
          to="/map"
          replace
        />
      ),
    },
  ]);