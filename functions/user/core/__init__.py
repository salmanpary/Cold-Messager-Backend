import json

def generate_response(status_code, message):
    return {
        'statusCode': status_code,
        'body': message
    }