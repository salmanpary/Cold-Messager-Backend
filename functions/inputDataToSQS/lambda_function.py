import json
import boto3

client = boto3.client('sqs')

def lambda_handler(event, context):
    try:
        body = event['dataBody']
        email = body['email']
        extracted_data = body['extractedData']
        message = body['message']
        client.send_message(QueueUrl="https://sqs.eu-north-1.amazonaws.com/942481252689/UserDataLambdaRDSQueue",MessageBody=json.dumps({
            'user':email,
            'extractedData':extracted_data,
            'message': message
        }))
        print('executed')
        return 'executed'
    except Exception as error:
        print(error)