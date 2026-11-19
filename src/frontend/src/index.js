import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import App from "./App";
import Home from "./pages/home.jsx";
import NotFound from "./pages/404.jsx";
import Register from "./pages/register.jsx";

import "./index.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
    errorElement: <NotFound />,
  },
  {
    path: "/registar",
    element: <Register />,
    errorElement: <NotFound />,
  }
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

