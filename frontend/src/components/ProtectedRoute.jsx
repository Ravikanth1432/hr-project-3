// src/ProtectedRoute.jsx
import React from "react";
import { Navigate } from "react-router-dom";
import jwtDecode  from "jwt-decode";

const ProtectedRoute = ({ children, roles }) => {
  const token = localStorage.getItem("token");

  if (!token) {
    // Not logged in at all → send to login
    return <Navigate to="/login" />;
  }

  try {
    const decoded = jwtDecode(token);
    const userRole = decoded.role;

    // If roles prop exists, check if user has one of them
    if (roles && !roles.includes(userRole)) {
      return <Navigate to="/login" />;
    }

    // ✅ Allowed → show the requested page
    return children;
  } catch (error) {
    console.error("Invalid token:", error);
    localStorage.removeItem("token");
    return <Navigate to="/login" />;
  }
};

export default ProtectedRoute;

/*import React from "react";
import { Navigate } from "react-router-dom";
import jwt_decode from "jwt-decode";

const ProtectedRoute = ({ children, allowedRoles }) => {
  const token = localStorage.getItem("token");
  if (!token) return <Navigate to="/" />;

  try {
    const decoded = jwt_decode(token);
    if (!allowedRoles.includes(decoded.role)) return <Navigate to="/" />;
  } catch (err) {
    return <Navigate to="/" />;
  }

  return children;
};

export default ProtectedRoute;*/