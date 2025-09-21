// frontend/src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import CandidateList from "./pages/CandidateList";
import CandidateForm from "./pages/CandidateForm";
import JobList from "./pages/JobList";
import JobDetails from "./pages/JobDetails";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        {/* ✅ Redirect root ("/") to login */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        <Route path="/login" element={<Login />} />
        <Route
          path="/candidates"
          element={
            <ProtectedRoute roles={["Admin", "Recruiter"]}>
              <CandidateList />
            </ProtectedRoute>
          }
        />
        <Route
          path="/candidate-form/:id"
          element={
            <ProtectedRoute roles={["Admin", "Recruiter"]}>
              <CandidateForm />
            </ProtectedRoute>
          }
        />
        <Route
          path="/candidate-form"
          element={
            <ProtectedRoute roles={["Admin", "Recruiter"]}>
              <CandidateForm />
            </ProtectedRoute>
          }
        />
        <Route
          path="/jobs"
          element={
            <ProtectedRoute roles={["Admin", "Recruiter", "HiringManager"]}>
              <JobList />
            </ProtectedRoute>
          }
        />
        <Route
          path="/jobs/:id"
          element={
            <ProtectedRoute roles={["Admin", "Recruiter", "HiringManager"]}>
              <JobDetails />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
