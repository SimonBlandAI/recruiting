import http.server
import json
import re
from urllib.parse import urlparse, parse_qs
from http import HTTPStatus

# Starter messages
starter_message_user_info = """
Thanks for interviewing with Bland! 
This endpoint is designed to test your ability to interact with customer API's.

We encourage the use of external tools like Postman to test this endpoint.

This endpoint is a POST request and requires the following:

POST https://us.api.bland.ai/recruiting/exampleApi/get-user-info

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

starter_message_book_appointment = """
This endpoint is a POST request for booking appointment times. 

We encourage the use of external tools like Postman to test this endpoint.

POST https://us.api.bland.ai/recruiting/exampleApi/book-appointment

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

error_message = """
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
    return api_key == "valid_api_key"

class BlandHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/get-user-info':
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({"error": "STARTING_ERROR", "message": starter_message_user_info})
            self.wfile.write(response.encode())
        elif parsed_path.path == '/book-appointment':
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({"error": "STARTING_ERROR_APPOINTMENT", "message": starter_message_book_appointment})
            self.wfile.write(response.encode())
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_path = urlparse(self.path)

        try:
            body = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON")
            return

        bland_api_key = self.headers.get('bland-api-key')
        content_type = self.headers.get('Content-Type')

        if not bland_api_key:
            self.send_error(HTTPStatus.UNAUTHORIZED, "Missing API key")
            return

        if content_type != 'application/json':
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid Content-Type")
            return

        if not validate_api_key(bland_api_key):
            self.send_error(HTTPStatus.UNAUTHORIZED, "Invalid API key")
            return

        if parsed_path.path == '/get-user-info':
            self.handle_get_user_info(body)
        elif parsed_path.path == '/book-appointment':
            self.handle_book_appointment(body)
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def handle_get_user_info(self, body):
        first_name = body.get('first_name')
        last_name = body.get('last_name')

        if not first_name or not last_name:
            self.send_error(HTTPStatus.BAD_REQUEST, "Missing first_name or last_name")
            return

        if not check_name_format(first_name) or not check_name_format(last_name):
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid name format")
            return

        response = {
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
        }

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def handle_book_appointment(self, body):
        first_name = body.get('first_name')
        last_name = body.get('last_name')
        interview_date = body.get('interview_date')
        interview_time = body.get('interview_time')

        if not all([first_name, last_name, interview_date, interview_time]):
            self.send_error(HTTPStatus.BAD_REQUEST, "Missing required fields")
            return

        if not check_name_format(first_name) or not check_name_format(last_name):
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid name format")
            return

        if not check_date_format(interview_date):
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid date format")
            return

        if not check_time_format(interview_time):
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid time format")
            return

        response = {"status": "success"}

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, BlandHandler)
    print("Server running on port 8000")
    httpd.serve_forever()