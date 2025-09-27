import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createApplicant } from '../api';

const AddApplicant = () => {
  const [formData, setFormData] = useState({
    name: '',
    languages: '',
    technologies: '',
    flagship_project: '',
    last_job: '',
    education: '',
    years_experience: '',
    resume_path: '',
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
      const data = await createApplicant(formData);
      if (data && !data.error) {
        navigate('/admin/users');
      } else {
        setError(data.error || 'Failed to add applicant');
      }
    } catch (err) {
      setError('Network error or server unreachable');
      console.error("Add applicant error:", err);
    }
  };

  return (
    <div className="container">
      <h1 className="display-4 mt-3 mb-3">Add Applicant</h1>
      <form onSubmit={handleSubmit}>
        {error && <div className="alert alert-danger">{error}</div>}
        <div className="mb-3">
          <label htmlFor="name" className="form-label">Name</label>
          <input type="text" className="form-control" id="name" name="name" value={formData.name} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label htmlFor="languages" className="form-label">Languages</label>
          <input type="text" className="form-control" id="languages" name="languages" value={formData.languages} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="technologies" className="form-label">Technologies</label>
          <input type="text" className="form-control" id="technologies" name="technologies" value={formData.technologies} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="flagship_project" className="form-label">Flagship Project</label>
          <input type="text" className="form-control" id="flagship_project" name="flagship_project" value={formData.flagship_project} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="last_job" className="form-label">Last Job</label>
          <input type="text" className="form-control" id="last_job" name="last_job" value={formData.last_job} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="education" className="form-label">Education</label>
          <input type="text" className="form-control" id="education" name="education" value={formData.education} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="years_experience" className="form-label">Years of Experience</label>
          <input type="number" className="form-control" id="years_experience" name="years_experience" value={formData.years_experience} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="resume_path" className="form-label">Resume Path</label>
          <input type="text" className="form-control" id="resume_path" name="resume_path" value={formData.resume_path} onChange={handleChange} required />
        </div>
        <button type="submit" className="btn btn-primary">Submit</button>
      </form>
    </div>
  );
};

export default AddApplicant;
