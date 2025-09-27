
const API_BASE_URL = 'http://127.0.0.1:5001'; // Your Flask backend URL

export const fetchWithAuth = async (endpoint, options = {}) => {
    const token = localStorage.getItem('access_token');
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (response.status === 401 || response.status === 302) {
        alert('Session expired or unauthorized. Please log in again.');
        localStorage.removeItem('access_token');
        window.location.href = '/login'; // Redirect to React login route
        return; // Prevent further processing
    }

    return response;
};

export const loginUser = async (email, password) => {
    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        body: formData,
    });
    const data = await response.json();
    if (response.ok) {
        localStorage.setItem('access_token', data.access_token);
        // Optionally store refresh token if you implement refresh logic
        // localStorage.setItem('refresh_token', data.refresh_token);
    }
    return { response, data };
};

export const registerUser = async (username, email, password, isAdmin) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('email', email);
    formData.append('password', password);
    if (isAdmin) {
        formData.append('is_admin', 'on');
    }

    const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        body: formData,
    });
    return response.json();
};

export const getJobs = async () => {
    const response = await fetchWithAuth('/jobs/');
    return response.json();
};

export const createJob = async (jobData) => {
    const formData = new FormData();
    for (const key in jobData) {
        formData.append(key, jobData[key]);
    }
    const response = await fetchWithAuth('/jobs/', {
        method: 'POST',
        body: formData,
    });
    return response.json();
};

export const getApplicants = async () => {
    const response = await fetchWithAuth('/applicants/');
    return response.json();
};

export const createApplicant = async (applicantData) => {
    const formData = new FormData();
    for (const key in applicantData) {
        formData.append(key, applicantData[key]);
    }
    const response = await fetchWithAuth('/applicants/', {
        method: 'POST',
        body: formData,
    });
    return response.json();
};

export const getUsers = async () => {
    const response = await fetchWithAuth('/users/');
    return response.json();
};

export const getUserDetails = async () => {
    const response = await fetchWithAuth('/auth/me');
    return response.json();
};
