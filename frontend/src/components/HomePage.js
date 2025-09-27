import React, { useEffect, useState } from 'react';
import { getJobs } from '../api';

const HomePage = () => {
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
      <h1 className="display-4 mt-3 mb-3">Available Jobs</h1>
      <div className="list-group">
        {jobs.length > 0 ? (
          jobs.map((job) => (
            <div key={job.id} className="list-group-item list-group-item-action">
              <div className="d-flex w-100 justify-content-between">
                <h5 className="mb-1">{job.title}</h5>
                <small>{job.work_location}</small>
              </div>
              <p className="mb-1">{job.description}</p>
              <small><strong>Required Technologies:</strong> {job.required_technologies}</small><br />
              <small><strong>Required Experience:</strong> {job.required_experience} years</small>
            </div>
          ))
        ) : (
          <p>No jobs available at the moment.</p>
        )}
      </div>
    </div>
  );
};

export default HomePage;
