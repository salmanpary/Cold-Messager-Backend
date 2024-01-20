import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from core import generate_response, load_env
from core.ColdMessage import ColdMessage

cred = credentials.Certificate(load_env())
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def lambda_handler(event, context):
    try:
        uid = event['uid']
        extracted_data = event['extractedData']
        user_record = db.collection('users-test').where(filter=FieldFilter('uid','==',uid)).get()
        if user_record:
            user_record_dict = user_record[0].to_dict()
            user_templates = user_record_dict['templates']
            if user_templates:
                for template in user_templates:
                    if template['default_template'] == True:
                        template_string = template['template_string']
                        new_message = ColdMessage(template_string,extracted_data)
                        return generate_response(200, new_message.generate_message())
            else:
                return generate_response(404, 'user does not have any default templates')
        return generate_response(404, 'User not found')
    except Exception as error:
        return generate_response(500, f'Internal Server Error: {error}')