import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from core import generate_response, load_env
from core.ColdMessage import ColdMessage
import json
import boto3

cred = credentials.Certificate(load_env())
app = firebase_admin.initialize_app(cred)
db = firestore.client()

client = boto3.client('lambda')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        email = body['email']
        extracted_data = body['extractedData']
        user_record = db.collection('users-test').where(filter=FieldFilter('email','==',email)).stream()
        if user_record:
            user_templates=None
            for doc in user_record:
                user_templates = doc.to_dict().get('templates', [])
            if user_templates:
                for template in user_templates:
                    if template.get('default_template', False):
                        template_string = template.get('template_string')
                        new_message = ColdMessage(template_string,extracted_data)
                        message = new_message.generate_message()
                        payload = {
                            "dataBody": {
                            "email":email,
                            "extractedData":extracted_data,
                            "message":message
                            }
                        }
                        client.invoke(FunctionName='inputDataToSQS',InvocationType="Event",Payload=json.dumps(payload),LogType="Tail")
                        return generate_response(200, message)
            else:
                return generate_response(404, 'user does not have any default templates')
        return generate_response(404, 'User not found')
    except Exception as error:
        return generate_response(500, f'Internal Server Error: {error}')