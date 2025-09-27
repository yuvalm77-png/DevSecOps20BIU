import React from 'react';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ children, isAdmin }) => {
  const isAuthenticated = localStorage.getItem('access_token');

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (!isAdmin) {
    // Optionally, redirect to a non-admin dashboard or show an unauthorized message
    return <Navigate to="/" replace />;
  }

  return children;
};

export default PrivateRoute;
