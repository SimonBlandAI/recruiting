from flask import Flask, request, jsonify
import re
from functools import wraps

app = Flask(__name__)

# Helper messages
starterMessageUserInfo = """
Thanks for interviewing with Bland! 
This endpoint is designed to test your ability to interact with customer API's.

We encourage the use of external tools like Postman to test this endpoint.

This endpoint is a POST request and requires the following:

POSThttps://recruiting-1.onrender.com/recruiting/exampleApi/get-user-info

1. Headers:
   - 'bland-api-key': A valid Bland API key (required)
   - 'Content-Type': application/json (required)

2. Request Body (JSON):
   - 'first_name': String, all lowercase, only letters (required)
   - 'last_name': String, all lowercase, only letters (required)

Example request:
POST /get-user-info
{
  "first_name": "john",
  "last_name": "doe"
}

Possible error responses:
- 401: Missing or invalid API key
- 400: Missing or incorrectly formatted first_name or last_name

A successful response will return user information if found.
"""

starterMessageBookAppointment = """
This endpoint is a POST request for getting appointment times. 

We encourage the use of external tools like Postman to test this endpoint.

First, switch this request to a POST request and remove the url parameters:

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

Example request:
POST /book-appointment
{
  "first_name": "john",
  "last_name": "doe",
  "interview_date": "15-06-2023",
  "interview_time": "14:30"
}

Possible error responses:
- 401: Missing or invalid API key
- 400: Missing or incorrectly formatted first_name, last_name, interview_date, or interview_time

A successful response will confirm the appointment booking.
"""

errorMessage = """
It seems like an error has occurred - either you're not on the right track and have managed to break this endpoint
or something is wrong with the endpoint itself. Please reach out to simon@bland.ai if you are certain that your request should be working.
"""

# Helper functions
def check_name_format(name):
    return bool(re.match(r'^[a-z]+$', name))

def check_date_format(date):
    return bool(re.match(r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$', date))

def check_time_format(time):
    return bool(re.match(r'^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', time))

def validate_api_key(api_key):
    # Simulating API key validation
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

def response_handler(status, data=None, errors=None):
    response = {"data": data, "errors": errors}
    return jsonify(response), status

@app.route('/recruiting/exampleApi/get-user-info', methods=['GET'])
def get_user_info_start():
    try:
        return response_handler(200, {
            "error": "STARTING_ERROR",
            "message": starterMessageUserInfo
        })
    except Exception:
        return response_handler(200, {
            "error": "UNEXPECTED_ERROR",
            "message": errorMessage
        })

@app.route('/recruiting/exampleApi/get-user-info', methods=['POST'])
@require_api_key
def get_user_info():
    try:
        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        errors = []

        if not first_name or not last_name:
            errors.append({
                "error": "MISSING_REQUIRED_BODY",
                "message": "Body 'first_name' and 'last_name' are required"
            })

        if first_name and last_name:
            if not isinstance(first_name, str) or not isinstance(last_name, str):
                errors.append({
                    "error": "INVALID_NAME_FORMAT",
                    "message": "Parameter first_name and last_name must be strings"
                })
            else:
                if not check_name_format(first_name):
                    errors.append({
                        "error": "INVALID_NAME_FORMAT",
                        "message": "Parameter first_name must be formatted correctly (all lowercase)"
                    })
                if not check_name_format(last_name):
                    errors.append({
                        "error": "INVALID_NAME_FORMAT",
                        "message": "Parameter last_name must be formatted correctly (all lowercase)"
                    })

        if errors:
            return response_handler(400, None, errors)

        return response_handler(200, {
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
        })
    except Exception:
        return response_handler(500, {
            "error": "UNEXPECTED_ERROR",
            "message": errorMessage
        })

@app.route('/recruiting/exampleApi/book-appointment', methods=['GET'])
def book_appointment_start():
    try:
        return response_handler(200, {
            "error": "STARTING_ERROR_APPOINTMENT",
            "message": starterMessageBookAppointment
        })
    except Exception:
        return response_handler(200, {
            "error": "UNEXPECTED_ERROR",
            "message": errorMessage
        })

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
            return response_handler(400, {
                "error": "MISSING_REQUIRED_BODY",
                "message": "All fields are required"
            })

        if not isinstance(first_name, str) or not isinstance(last_name, str):
            return response_handler(400, {
                "error": "INVALID_NAME_FORMAT",
                "message": "Parameter first_name and last_name must be strings"
            })

        if not check_name_format(first_name):
            return response_handler(400, {
                "error": "INVALID_NAME_FORMAT",
                "message": "Parameter first_name must be formatted correctly (all lowercase)"
            })

        if not check_name_format(last_name):
            return response_handler(400, {
                "error": "INVALID_NAME_FORMAT",
                "message": "Parameter last_name must be formatted correctly (all lowercase)"
            })

        if not check_date_format(interview_date):
            return response_handler(400, {
                "error": "INVALID_DATE_FORMAT",
                "message": "Parameter interview_date must be formatted correctly (DD-MM-YYYY)"
            })

        if not check_time_format(interview_time):
            return response_handler(400, {
                "error": "INVALID_TIME_FORMAT",
                "message": "Parameter interview_time must be formatted correctly (HH:MM in 24-hour time)"
            })

        return response_handler(200, {
            "status": "success"
        })
    except Exception:
        return response_handler(500, {
            "error": "UNEXPECTED_ERROR",
            "message": errorMessage
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)