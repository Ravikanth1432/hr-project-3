// frontend/src/pages/JobDetails.jsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const JobDetails = () => {
  const { id } = useParams();
  const [job, setJob] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/jobs/${id}`)
      .then((res) => res.json())
      .then(setJob)
      .catch(console.error);
  }, [id]);

  if (!job) return <p>Loading job details...</p>;

  return (
    <div className="max-w-2xl mx-auto bg-white shadow-lg rounded-xl p-8">
      <h2 className="text-2xl font-bold text-indigo-600 mb-4">{job.title}</h2>
      <p className="mb-4">{job.description}</p>
      <h3 className="text-lg font-semibold mb-2">Candidates</h3>
      <ul className="list-disc list-inside">
        {job.candidates?.length > 0 ? (
          job.candidates.map((c) => (
            <li key={c.id}>
              {c.name} - {c.email}
            </li>
          ))
        ) : (
          <p>No candidates applied yet.</p>
        )}
      </ul>
    </div>
  );
};

export default JobDetails;

/*import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import API from "../api";

const JobDetails = () => {
  const { id } = useParams();
  const [job, setJob] = useState(null);

  useEffect(() => {
    API.get(`/jobs/${id}`)
      .then((res) => setJob(res.data))
      .catch((err) => console.error(err));
  }, [id]);

  if (!job) return <div>Loading...</div>;

  return (
    <div>
      <h2>{job.title}</h2>
      <p>{job.required_skills}</p>
      <p>{job.description}</p>
    </div>
  );
};

export default JobDetails;*/