import React, { useEffect, useState } from 'react';
import { getJobs } from '../api';
import { Link } from 'react-router-dom';

const ManageJobs = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const data = await getJobs();
        setJobs(data);
      } catch (err) {
        setError('Failed to fetch jobs.');
        console.error("Error fetching jobs:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, []);

  if (loading) {
    return <div className="text-center mt-5">Loading jobs...</div>;
  }

  if (error) {
    return <div className="alert alert-danger mt-5">{error}</div>;
  }

  return (
    <div className="container">
      <h1 className="display-4 mt-3 mb-3">Manage Jobs</h1>
      <div className="d-flex justify-content-end mb-3">
        <Link to="/admin/add_job" className="btn btn-primary">Add Job</Link>
      </div>

      <table className="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Employment Type</th>
            <th>Work Location</th>
            <th>Is Open</th>
          </tr>
        </thead>
        <tbody>
          {jobs.length > 0 ? (
            jobs.map((job) => (
              <tr key={job.id}>
                <td>{job.id}</td>
                <td>{job.title}</td>
                <td>{job.employment_type}</td>
                <td>{job.work_location}</td>
                <td>{job.is_open ? 'Yes' : 'No'}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5">No jobs found.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default ManageJobs;
