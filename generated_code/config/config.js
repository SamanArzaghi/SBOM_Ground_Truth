// config.js
// This file contains configuration settings for the application.
// Each setting can be configured via environment variables for flexibility across different environments.

const config = {
    // Base URL for API requests. Can be set via the API_BASE_URL environment variable.
    apiBaseUrl: process.env.API_BASE_URL || 'https://api.example.com',

    // Timeout for API requests in milliseconds. Configurable via the API_TIMEOUT environment variable.
    timeout: parseInt(process.env.API_TIMEOUT, 10) || 5000,

    // Current environment of the application. Defaults to 'development'.
    environment: process.env.NODE_ENV || 'development',

    logging: {
        // Log level for the application. Configurable via the LOG_LEVEL environment variable.
        level: process.env.LOG_LEVEL || 'info',

        // Enable or disable logging. Controlled via the LOGGING_ENABLED environment variable.
        enabled: process.env.LOGGING_ENABLED !== 'false'
    },

    featureFlags: {
        // Toggle for enabling new features. Managed via the ENABLE_NEW_FEATURE environment variable.
        enableNewFeature: process.env.ENABLE_NEW_FEATURE === 'true'
    }
};

module.exports = config;