import boto3
import json

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    
    dynamo = boto3.client('dynamodb')
    
    query_params = {
        'TableName': 'driver_speed',
        'KeyConditionExpression': 'driverID = :pk_value AND speed_time BETWEEN :sk_value1 AND :sk_value2',
        'ExpressionAttributeValues': {
            ':pk_value': {'S': 'zouan1000007'},
            ':sk_value1': {'S': '2017-01-01T08:00:10.000'},
            ':sk_value2': {'S': '2017-01-01T08:02:30.000'}
        },
        'Limit': 10  # Limit the result to 10 items
    }
    
    # Query the table
    response = dynamo.query(**query_params)
    return respond(None, response)
