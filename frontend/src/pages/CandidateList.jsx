// frontend/src/pages/CandidateList.jsx
import React, { useEffect, useState } from "react";
import API from "../api";
import { Link } from "react-router-dom";
import jwt_decode from "jwt-decode";

const CandidateList = () => {
  const [candidates, setCandidates] = useState([]);
  const [role, setRole] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) setRole(jwt_decode(token).role);

    API.get("/candidates")
      .then((res) => setCandidates(res.data))
      .catch((err) => console.error(err));
  }, []);

  const handleDelete = async (id) => {
    try {
      await API.delete(`/candidates/${id}`);
      setCandidates(candidates.filter((c) => c.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Candidates</h2>
      <Link to="/candidate-form">Add Candidate</Link>
      <ul>
        {candidates.map((c) => (
          <li key={c.id}>
            {c.name} - {c.email} - {c.current_status}{" "}
            {role === "Admin" && (
              <button onClick={() => handleDelete(c.id)}>Delete</button>
            )}
            {["Admin", "Recruiter"].includes(role) && (
              <Link to={`/candidate-form/${c.id}`}>Edit</Link>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CandidateList;