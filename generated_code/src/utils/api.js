// src/utils/api.js

import axios from 'axios';

/**
 * API utility functions for making HTTP requests.
 */

/**
 * Create an Axios instance with default configuration.
 * The baseURL is set using environment variables to allow for different environments (development, staging, production).
 */
const apiClient = axios.create({
  baseURL: process.env.API_BASE_URL || 'https://api.example.com', // Use environment variable or default
  timeout: process.env.API_TIMEOUT || 5000, // Configurable timeout with a default value
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Function to perform a GET request.
 * @param {string} endpoint - The API endpoint to request.
 * @param {object} [params={}] - Optional query parameters.
 * @returns {Promise} - Promise representing the HTTP response.
 * @throws {Error} - Throws an error if the request fails.
 */
export const get = async (endpoint, params = {}) => {
  try {
    const response = await apiClient.get(endpoint, { params });
    return response.data;
  } catch (error) {
    handleError('GET', endpoint, error);
  }
};

/**
 * Function to perform a POST request.
 * @param {string} endpoint - The API endpoint to request.
 * @param {object} data - The data to send in the request body.
 * @returns {Promise} - Promise representing the HTTP response.
 * @throws {Error} - Throws an error if the request fails.
 */
export const post = async (endpoint, data) => {
  try {
    const response = await apiClient.post(endpoint, data);
    return response.data;
  } catch (error) {
    handleError('POST', endpoint, error);
  }
};

/**
 * Function to perform a PUT request.
 * @param {string} endpoint - The API endpoint to request.
 * @param {object} data - The data to send in the request body.
 * @returns {Promise} - Promise representing the HTTP response.
 * @throws {Error} - Throws an error if the request fails.
 */
export const put = async (endpoint, data) => {
  try {
    const response = await apiClient.put(endpoint, data);
    return response.data;
  } catch (error) {
    handleError('PUT', endpoint, error);
  }
};

/**
 * Function to perform a DELETE request.
 * @param {string} endpoint - The API endpoint to request.
 * @returns {Promise} - Promise representing the HTTP response.
 * @throws {Error} - Throws an error if the request fails.
 */
export const remove = async (endpoint) => {
  try {
    const response = await apiClient.delete(endpoint);
    return response.data;
  } catch (error) {
    handleError('DELETE', endpoint, error);
  }
};

/**
 * Handle errors for API requests.
 * @param {string} method - The HTTP method used for the request.
 * @param {string} endpoint - The API endpoint that was requested.
 * @param {Error} error - The error object caught during the request.
 * @throws {Error} - Throws a categorized error with additional context.
 */
const handleError = (method, endpoint, error) => {
  if (error.response) {
    // Server responded with a status other than 2xx
    console.error(`${method} request to ${endpoint} failed with status ${error.response.status}:`, error.response.data);
  } else if (error.request) {
    // Request was made but no response received
    console.error(`${method} request to ${endpoint} failed: No response received`, error.request);
  } else {
    // Something happened in setting up the request
    console.error(`${method} request to ${endpoint} failed:`, error.message);
  }
  throw error;
};