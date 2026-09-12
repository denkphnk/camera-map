import { createBrowserRouter } from "react-router-dom";

import { LoginPage } from "../pages/LoginPage/LoginPage";
import { RegisterPage } from "../pages/RegisterPage/RegisterPage";
import { MapPage } from "../pages/MapPage/MapPage";
import { LocationPage } from "../pages/LocationPage/LocationPage";
import { ProfilePage } from "../pages/ProfilePage/ProfilePage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <LoginPage />,
  },
  {
    path: "/register",
    element: <RegisterPage />,
  },
  {
    path: "/map",
    element: <MapPage />,
  },
  {
    path: "/location/:cameraId",
    element: <LocationPage />,
  },
  {
    path: "/profile",
    element: <ProfilePage />,
  },
]);