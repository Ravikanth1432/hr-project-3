// frontend/src/pages/JobList.jsx
import React, { useState, useEffect } from "react";
import API from "../api";
import { Link } from "react-router-dom";

const JobList = () => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    API.get("/jobs")
      .then((res) => setJobs(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2>Jobs</h2>
      <Link to="/job-form">Add Job</Link>
      <ul>
        {jobs.map((j) => (
          <li key={j.id}>
            {j.title} - {j.required_skills} <Link to={`/jobs/${j.id}`}>Details</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default JobList;