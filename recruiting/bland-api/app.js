const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

// Helper functions
function checkNameFormat(name) {
  return /^[a-z]+$/.test(name);
}

function checkDateFormat(date) {
  return /^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$/.test(date);
}

function checkTimeFormat(time) {
  return /^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/.test(time);
}

function validateApiKey(apiKey) {
  return apiKey && apiKey.startsWith('sk-');
}

// Middleware for API key validation
function requireApiKey(req, res, next) {
  const apiKey = req.header('bland-api-key');
  if (!validateApiKey(apiKey)) {
    return res.status(401).json({
      error: 'INVALID_API_KEY',
      message: 'The API key provided is invalid or missing. It should start with \'sk-\'.'
    });
  }
  next();
}

// GET /get-user-info
app.get('/get-user-info', (req, res) => {
  res.json({
    message: "This endpoint is for getting user info. Use POST method with 'first_name' and 'last_name' in the request body. Remember to include your API key starting with 'sk-' in the 'bland-api-key' header."
  });
});

// POST /get-user-info
app.post('/get-user-info', requireApiKey, (req, res) => {
  const { first_name, last_name } = req.body;

  if (!first_name || !last_name) {
    return res.status(400).json({
      error: 'MISSING_FIELDS',
      message: 'Both first_name and last_name are required'
    });
  }

  if (!checkNameFormat(first_name) || !checkNameFormat(last_name)) {
    return res.status(400).json({
      error: 'INVALID_NAME_FORMAT',
      message: 'Names must be all lowercase letters'
    });
  }

  res.json({
    jobId: '1234567890',
    jobTitle: 'Support Engineer',
    jobDescription: 'Support Engineering at Bland',
    applicantInformation: {
      applicationId: '1234567890',
      firstName: first_name,
      lastName: last_name,
      email: `${first_name}@bland.ai`,
      dateApplied: new Date().toISOString(),
      phone_number: '+1 131 255 0123',
      linkedin_url: `https://www.linkedin.com/in/${first_name}-bland-0000000000`,
    }
  });
});

// GET /book-appointment
app.get('/book-appointment', (req, res) => {
  res.json({
    message: "This endpoint is for booking appointments. Use POST method with 'first_name', 'last_name', 'interview_date', and 'interview_time' in the request body. Remember to include your API key starting with 'sk-' in the 'bland-api-key' header."
  });
});

// POST /book-appointment
app.post('/book-appointment', requireApiKey, (req, res) => {
  const { first_name, last_name, interview_date, interview_time } = req.body;

  if (!first_name || !last_name || !interview_date || !interview_time) {
    return res.status(400).json({
      error: 'MISSING_FIELDS',
      message: 'All fields are required'
    });
  }

  if (!checkNameFormat(first_name) || !checkNameFormat(last_name)) {
    return res.status(400).json({
      error: 'INVALID_NAME_FORMAT',
      message: 'Names must be all lowercase letters'
    });
  }

  if (!checkDateFormat(interview_date)) {
    return res.status(400).json({
      error: 'INVALID_DATE_FORMAT',
      message: 'Date must be in DD-MM-YYYY format'
    });
  }

  if (!checkTimeFormat(interview_time)) {
    return res.status(400).json({
      error: 'INVALID_TIME_FORMAT',
      message: 'Time must be in HH:MM 24-hour format'
    });
  }

  res.json({
    status: 'success',
    message: 'Appointment booked successfully'
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'UNEXPECTED_ERROR',
    message: 'An unexpected error occurred. Please try again later.'
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});