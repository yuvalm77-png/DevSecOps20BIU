import React from 'react';
import { Link } from 'react-router-dom';

const AdminDashboard = () => {
  return (
    <div className="container">
      <h1 className="display-4 mt-3 mb-3">Admin Dashboard</h1>
      <div className="list-group">
        <Link to="/admin/users" className="list-group-item list-group-item-action">Manage Users</Link>
        <Link to="/admin/jobs" className="list-group-item list-group-item-action">Manage Jobs</Link>
      </div>
    </div>
  );
};

export default AdminDashboard;
