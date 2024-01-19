import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from core import generate_response

cred = credentials.Certificate('./credentials.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def lambda_handler(event, context):
    try:
        uid = event['uid']
        user_record = db.collection('users-test').where(filter=FieldFilter('uid','==',uid)).get()
        if user_record:
            user_record_dict = user_record[0].to_dict()
            user_templates = user_record_dict['templates']
            if user_templates:
                for template in user_templates:
                    if template['default_template'] == True:
                        return generate_response(200, template)
            else:
                return generate_response(404, 'user does not have any templates')
        return generate_response(404, 'User not found')
    except:
        return generate_response(500, 'Internal Server Error')