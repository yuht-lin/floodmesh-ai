import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchHealth = () => api.get('/health');
export const fetchIncidents = (params) => api.get('/incidents', { params });
export const fetchResources = (params) => api.get('/resources', { params });
export const fetchAllocations = () => api.get('/allocations');
export const recalculateAllocations = () => api.post('/allocations/recalculate');
export const ingestReport = (report_text, source = 'citizen_hotline') =>
  api.post('/incidents/ingest-report', { report_text, source });
export const approveAssignment = (assignment_id, responder_notes = '') =>
  api.post(`/assignments/${assignment_id}/approve`, { responder_notes });
export const rejectAssignment = (assignment_id, reason) =>
  api.post(`/assignments/${assignment_id}/reject`, { reason });
export const modifyAssignment = (assignment_id, new_resource_id, reason) =>
  api.post(`/assignments/${assignment_id}/modify`, { new_resource_id, reason });

export default api;
