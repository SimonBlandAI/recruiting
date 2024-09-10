from flask import Flask, request, jsonify
from functools import wraps
import re

app = Flask(__name__)

# Helper functions
def check_name_format(name):
    return bool(re.match(r'^[a-z]+$', name))

def check_date_format(date):
    return bool(re.match(r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$', date))

def check_time_format(time):
    return bool(re.match(r'^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', time))

def validate_api_key(api_key):
    # Simulating API key validation
    return api_key == "valid_api_key"

# Decorator for API key validation
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('bland-api-key')
        if not api_key or not validate_api_key(api_key):
            return jsonify({"error": "INVALID_API_KEY", "message": "The API key provided is invalid or missing"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/get-user-info', methods=['GET'])
def get_user_info_start():
    return jsonify({
        "message": "This endpoint is for getting user info. Use POST method with 'first_name' and 'last_name' in the request body."
    })

@app.route('/get-user-info', methods=['POST'])
@require_api_key
def get_user_info():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not first_name or not last_name:
        return jsonify({"error": "MISSING_FIELDS", "message": "Both first_name and last_name are required"}), 400

    if not check_name_format(first_name) or not check_name_format(last_name):
        return jsonify({"error": "INVALID_NAME_FORMAT", "message": "Names must be all lowercase letters"}), 400

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
    })

@app.route('/book-appointment', methods=['GET'])
def book_appointment_start():
    return jsonify({
        "message": "This endpoint is for booking appointments. Use POST method with 'first_name', 'last_name', 'interview_date', and 'interview_time' in the request body."
    })

@app.route('/book-appointment', methods=['POST'])
@require_api_key
def book_appointment():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    interview_date = data.get('interview_date')
    interview_time = data.get('interview_time')

    if not all([first_name, last_name, interview_date, interview_time]):
        return jsonify({"error": "MISSING_FIELDS", "message": "All fields are required"}), 400

    if not check_name_format(first_name) or not check_name_format(last_name):
        return jsonify({"error": "INVALID_NAME_FORMAT", "message": "Names must be all lowercase letters"}), 400

    if not check_date_format(interview_date):
        return jsonify({"error": "INVALID_DATE_FORMAT", "message": "Date must be in DD-MM-YYYY format"}), 400

    if not check_time_format(interview_time):
        return jsonify({"error": "INVALID_TIME_FORMAT", "message": "Time must be in HH:MM 24-hour format"}), 400

    return jsonify({"status": "success", "message": "Appointment booked successfully"})

if __name__ == '__main__':
    app.run(debug=True)