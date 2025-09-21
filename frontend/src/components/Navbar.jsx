// frontend/src/components/Navbar.jsx
import React from "react";
import { Link, useNavigate } from "react-router-dom";
import jwt_decode from "jwt-decode";

function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  let role = null;

  if (token) {
    try {
      role = jwt_decode(token).role;
    } catch (err) {
      role = null;
    }
  }
  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav style={{ padding: "10px", borderBottom: "1px solid #ccc" }}>
      {role && ["Admin", "Recruiter"].includes(role) && (
        <Link to="/candidates" style={{ marginRight: "10px" }}>Candidates</Link>
      )}
      {role && ["Admin", "Recruiter", "HiringManager"].includes(role) && (
        <Link to="/jobs" style={{ marginRight: "10px" }}>Jobs</Link>
      )}
      {role && <button onClick={handleLogout}>Logout</button>}
    </nav>
  );
}

export default Navbar;