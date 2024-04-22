import boto3
import csv, json

bucket = 'comp4442sparkapp'

def lambda_handler(event, context):
    
    try:
        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket(bucket)
        prefix_objs = my_bucket.objects.filter(Prefix="results/csv")
        
        prefix_df = []
    
        for obj in prefix_objs:
            key = obj.key
            if key.endswith(".csv"):
                lines = str(obj.get()['Body'].read().decode('utf-8')).split()
                for row in csv.DictReader(lines):
                    prefix_df.append(row)
                    
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(prefix_df)
        }
        
    except Exception as e:
        print(e)
        print('Error getting object from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(bucket))
        raise e
