import boto3
import json

driver_list = ['zouan1000007', 'duxu1000009', 'hanhui1000002', 'panxian1000005', 'haowei1000008', \
                'shenxian1000004', 'likun1000003', 'zengpeng1000000', 'xiezhi1000006', 'xiexiao1000001']

def lambda_handler(event, context):
    
    http_method = event['requestContext']['http']['method']
    
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': ''
        }
    elif http_method == 'GET':
        query_params = event['queryStringParameters']
        startTime = query_params['startTime']
        endTime = query_params['endTime']

    elif http_method == 'POST':
        body = json.loads(event['body'])
        startTime = body['startTime']
        endTime = body['endTime']
    
    dynamo = boto3.client('dynamodb')
    
    responseList = []
    
    for i in range(len(driver_list)):
        query_params = {
            'TableName': 'driver_speed',
            'KeyConditionExpression': 'driverID = :pk_value AND speed_time BETWEEN :sk_value1 AND :sk_value2',
            'ExpressionAttributeValues': {
                ':pk_value': {'S': driver_list[i]},
                ':sk_value1': {'S': startTime},
                ':sk_value2': {'S': endTime}
            }
        }
        # Query the table
        responseList.append(dynamo.query(**query_params))
        
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(responseList)
    }
