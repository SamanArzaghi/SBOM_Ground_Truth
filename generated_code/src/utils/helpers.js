// src/utils/helpers.js

// This file provides utility functions to be used across the project, leveraging lodash for common operations.

const _ = require('lodash');

/**
 * Function to capitalize the first letter of each word in a string.
 * @param {string} str - The string to be capitalized.
 * @returns {string} - The capitalized string, or the original input if it's not a string.
 */
function capitalizeWords(str) {
    if (!_.isString(str) || str === null || str === undefined) {
        return str || '';
    }
    return _.startCase(_.toLower(str));
}

module.exports = {
    capitalizeWords
};