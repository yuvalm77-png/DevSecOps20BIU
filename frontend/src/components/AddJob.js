import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createJob } from '../api';

const AddJob = () => {
  const [formData, setFormData] = useState({
    title: '',
    employment_type: '',
    work_location: '',
    description: '',
    required_technologies: '',
    required_experience: '',
  });
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    try {
      const data = await createJob(formData);
      if (data && !data.error) {
        navigate('/admin/jobs');
      } else {
        setError(data.error || 'Failed to add job');
      }
    } catch (err) {
      setError('Network error or server unreachable');
      console.error("Add job error:", err);
    }
  };

  return (
    <div className="container">
      <h1 className="display-4 mt-3 mb-3">Add Job</h1>
      <form onSubmit={handleSubmit}>
        {error && <div className="alert alert-danger">{error}</div>}
        <div className="mb-3">
          <label htmlFor="title" className="form-label">Title</label>
          <input type="text" className="form-control" id="title" name="title" value={formData.title} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label htmlFor="employment_type" className="form-label">Employment Type</label>
          <input type="text" className="form-control" id="employment_type" name="employment_type" value={formData.employment_type} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="work_location" className="form-label">Work Location</label>
          <input type="text" className="form-control" id="work_location" name="work_location" value={formData.work_location} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="description" className="form-label">Description</label>
          <textarea className="form-control" id="description" name="description" value={formData.description} onChange={handleChange}></textarea>
        </div>
        <div className="mb-3">
          <label htmlFor="required_technologies" className="form-label">Required Technologies</label>
          <input type="text" className="form-control" id="required_technologies" name="required_technologies" value={formData.required_technologies} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="required_experience" className="form-label">Required Experience</label>
          <input type="number" className="form-control" id="required_experience" name="required_experience" value={formData.required_experience} onChange={handleChange} />
        </div>
        <button type="submit" className="btn btn-primary">Submit</button>
      </form>
    </div>
  );
};

export default AddJob;
