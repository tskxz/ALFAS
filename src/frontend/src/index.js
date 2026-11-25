import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import App from "./App";
import Início from "./pages/home.jsx";
import NotFound from "./pages/404.jsx";
import Registar from "./pages/register.jsx";
import Entrar from "./pages/login.jsx";

import "./index.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Início />,
    errorElement: <NotFound />,
  },
  {
    path: "/registar",
    element: <Registar />,
    errorElement: <NotFound />,
  },
  {
    path: "/entrar",
    element: <Entrar />,
    errorElement: <NotFound />,
  }
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

