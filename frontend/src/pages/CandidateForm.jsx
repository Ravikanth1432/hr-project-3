// frontend/src/pages/CandidateForm.jsx
import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import API from "../api";

const CandidateForm = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [status, setStatus] = useState("");
  const [resume, setResume] = useState("");

  const navigate = useNavigate();
  const { id } = useParams();

  useEffect(() => {
    if (id) {
      API.get(`/candidates/${id}`).then((res) => {
        const c = res.data;
        setName(c.name);
        setEmail(c.email);
        setPhone(c.phone_number);
        setStatus(c.current_status);
        setResume(c.resume_link);
      });
    }
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      name,
      email,
      phone_number: phone,
      current_status: status,
      resume_link: resume,
    };
    try {
      if (id) await API.put(`/candidates/${id}`, payload);
      else await API.post("/candidates", payload);
      navigate("/candidates");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h2>{id ? "Edit Candidate" : "Add Candidate"}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input value={name} onChange={(e) => setName(e.target.value)} />
        </div>
        <div>
          <label>Email:</label>
          <input value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>
        <div>
          <label>Phone:</label>
          <input value={phone} onChange={(e) => setPhone(e.target.value)} />
        </div>
        <div>
          <label>Status:</label>
          <input value={status} onChange={(e) => setStatus(e.target.value)} />
        </div>
        <div>
          <label>Resume Link:</label>
          <input value={resume} onChange={(e) => setResume(e.target.value)} />
        </div>
        <button type="submit">{id ? "Update" : "Add"}</button>
      </form>
    </div>
  );
};

export default CandidateForm;