from flask import Flask, request, jsonify
import re
from functools import wraps

app = Flask(__name__)

# Helper messages
starterMessageUserInfo = """
This endpoint is a POST request and requires the following:

POST https://recruiting-1.onrender.com/recruiting/exampleApi/get-user-info

1. Headers:
   - 'bland-api-key': A valid Bland API key (required)
   - 'Content-Type': application/json (required)

2. Request Body (JSON):
   - 'first_name': String, all lowercase, only letters (required)
   - 'last_name': String, all lowercase, only letters (required)

Possible error responses:
- 401: Missing or invalid API key
- 400: Missing or incorrectly formatted first_name or last_name

A successful response will return user information if found.
"""

starterMessageBookAppointment = """
This endpoint is a POST request for booking appointments:

POST https://recruiting-1.onrender.com/recruiting/exampleApi/book-appointment

This endpoint requires the following:

1. Headers:
   - 'bland-api-key': A valid Bland API key (required)
   - 'Content-Type': application/json (required)

2. Request Body (JSON):
   - 'first_name': String, all lowercase, only letters (required)
   - 'last_name': String, all lowercase, only letters (required)
   - 'interview_date': String, format DD-MM-YYYY (required)
   - 'interview_time': String, format HH:MM in 24-hour time (required)

Possible error responses:
- 401: Missing or invalid API key
- 400: Missing or incorrectly formatted first_name, last_name, interview_date, or interview_time

A successful response will confirm the appointment booking.
"""

errorMessage = "An unexpected error occurred. Please contact support if you believe this is a mistake."

# Helper functions
def check_name_format(name):
    return bool(re.match(r'^[a-z]+$', name))

def check_date_format(date):
    return bool(re.match(r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$', date))

def check_time_format(time):
    return bool(re.match(r'^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', time))

def validate_api_key(api_key):
    return api_key.startswith("sk-")

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('bland-api-key')
        if not api_key or not validate_api_key(api_key):
            return jsonify({
                "error": "INVALID_API_KEY",
                "message": "The API key provided is invalid or missing"
            }), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/recruiting/exampleApi/get-user-info', methods=['GET'])
def get_user_info_start():
    return jsonify({"message": starterMessageUserInfo}), 200

@app.route('/recruiting/exampleApi/get-user-info', methods=['POST'])
@require_api_key
def get_user_info():
    try:
        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if not first_name or not last_name:
            return jsonify({
                "error": "MISSING_REQUIRED_BODY",
                "message": "Body 'first_name' and 'last_name' are required"
            }), 400

        if not isinstance(first_name, str) or not isinstance(last_name, str):
            return jsonify({
                "error": "INVALID_NAME_FORMAT",
                "message": "Parameters first_name and last_name must be strings"
            }), 400

        if not check_name_format(first_name) or not check_name_format(last_name):
            return jsonify({
                "error": "INVALID_NAME_FORMAT",
                "message": "Parameters first_name and last_name must be formatted correctly (all lowercase)"
            }), 400

        return jsonify({
            "jobId": "1234567890",
            "jobTitle": "Support Engineer",
            "jobDescription": "Support Engineering at Bland",
            "applicantInformation": {
                "applicationId": "1234567890",
                "firstName": first_name,
                "lastName": last_name,
                "email": f"{first_name}@bland.ai",
                "dateApplied": "2023-09-09T00:00:00Z",
                "phone_number": "+1 131 255 0123",
                "linkedin_url": f"https://www.linkedin.com/in/{first_name}-bland-0000000000",
            }
        }), 200
    except Exception:
        return jsonify({
            "error": "UNEXPECTED_ERROR",
            "message": errorMessage
        }), 500

@app.route('/recruiting/exampleApi/book-appointment', methods=['GET'])
def book_appointment_start():
    return jsonify({"message": starterMessageBookAppointment}), 200

@app.route('/recruiting/exampleApi/book-appointment', methods=['POST'])
@require_api_key
def book_appointment():
    try:
        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        interview_date = data.get('interview_date')
        interview_time = data.get('interview_time')

        if not all([first_name, last_name, interview_date, interview_time]):
            return jsonify({
                "error": "MISSING_REQUIRED_BODY",
                "message": "All fields (first_name, last_name, interview_date, interview_time) are required"
            }), 400

        if not isinstance(first_name, str) or not isinstance(last_name, str):
            return jsonify({
                "error": "INVALID_NAME_FORMAT",
                "message": "Parameters first_name and last_name must be strings"
            }), 400

        if not check_name_format(first_name) or not check_name_format(last_name):
            return jsonify({
                "error": "INVALID_NAME_FORMAT",
                "message": "Parameters first_name and last_name must be formatted correctly (all lowercase)"
            }), 400

        if not check_date_format(interview_date):
            return jsonify({
                "error": "INVALID_DATE_FORMAT",
                "message": "Parameter interview_date must be formatted correctly (DD-MM-YYYY)"
            }), 400

        if not check_time_format(interview_time):
            return jsonify({
                "error": "INVALID_TIME_FORMAT",
                "message": "Parameter interview_time must be formatted correctly (HH:MM in 24-hour time)"
            }), 400

        return jsonify({
            "message": "Appointment booked successfully",
            "appointment": {
                "first_name": first_name,
                "last_name": last_name,
                "interview_date": interview_date,
                "interview_time": interview_time
            }
        }), 200
    except Exception:
        return jsonify({
            "error": "UNEXPECTED_ERROR",
            "message": errorMessage
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)