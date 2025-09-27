import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './components/HomePage';
import Login from './components/Login';
import Register from './components/Register';
import AdminDashboard from './components/AdminDashboard';
import ManageUsers from './components/ManageUsers';
import ManageJobs from './components/ManageJobs';
import AddApplicant from './components/AddApplicant';
import AddJob from './components/AddJob';
import PrivateRoute from './components/PrivateRoute';
import { getUserDetails } from './api';

function App() {
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAdminStatus = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const user = await getUserDetails();
          setIsAdmin(user.is_admin);
        } catch (error) {
          console.error("Failed to fetch user details:", error);
          localStorage.removeItem('access_token');
          setIsAdmin(false);
        }
      }
      setLoading(false);
    };
    checkAdminStatus();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      <Navbar isAdmin={isAdmin} />
      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<Login setIsAdmin={setIsAdmin} />} />
          <Route path="/register" element={<Register />} />

          {/* Admin Routes */}
          <Route
            path="/admin"
            element={
              <PrivateRoute isAdmin={isAdmin}>
                <AdminDashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/admin/users"
            element={
              <PrivateRoute isAdmin={isAdmin}>
                <ManageUsers />
              </PrivateRoute>
            }
          />
          <Route
            path="/admin/jobs"
            element={
              <PrivateRoute isAdmin={isAdmin}>
                <ManageJobs />
              </PrivateRoute>
            }
          />
          <Route
            path="/admin/add_applicant"
            element={
              <PrivateRoute isAdmin={isAdmin}>
                <AddApplicant />
              </PrivateRoute>
            }
          />
          <Route
            path="/admin/add_job"
            element={
              <PrivateRoute isAdmin={isAdmin}>
                <AddJob />
              </PrivateRoute>
            }
          />

          {/* Redirect any unmatched routes to home or login if not authenticated */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;