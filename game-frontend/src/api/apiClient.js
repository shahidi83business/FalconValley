import axios from 'axios';

const STATUS_MESSAGES = {
  400: 'The request could not be processed. Please check your input.',
  401: 'Your session has expired or your credentials are invalid. Please sign in again.',
  403: 'You do not have permission to perform this action.',
  404: 'The requested resource was not found.',
  409: 'This action conflicts with existing data.',
  422: 'Some fields are invalid. Please review and try again.',
  429: 'Too many requests. Please wait a moment and try again.',
  500: 'The server ran into a problem. Please try again later.',
  502: 'The service is temporarily unavailable. Please try again later.',
  503: 'The service is temporarily unavailable. Please try again later.',
  504: 'The request timed out. Please try again later.',
};

export const getApiErrorMessage = (error) => {
  if (error.response) {
    const { status, data } = error.response;
    return data?.message || data?.error || STATUS_MESSAGES[status] || 'Something went wrong. Please try again.';
  }

  if (error.request) {
    return 'Unable to reach the server. Please check your connection and try again.';
  }

  return error.message || 'Something went wrong. Please try again.';
};

const apiClient = axios.create();

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status;
    const message = getApiErrorMessage(error);

    error.userMessage = message;

    if (!error.config?.suppressErrorPopup && typeof window !== 'undefined') {
      window.alert(status ? `Error ${status}: ${message}` : message);
    }

    return Promise.reject(error);
  }
);

export default apiClient;
