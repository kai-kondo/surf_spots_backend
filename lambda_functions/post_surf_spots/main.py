import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SurfSpots')

def lambda_handler(event, context):
    # リクエストイベント全体をログ出力する
    print(json.dumps(event))

    try:
        body = json.loads(event['body'])

        item = {
            'spot_id': f"{body['spot_name']}_{body['location']}",
            'location': body['location'],
            'spot_name': body['spot_name'],
            'description': body['description'],
            'media_url': body['media_url']
        }

        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps('Spot successfully added!')
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f"KeyError: {str(e)}")
        }
    except Exception as ex:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Internal Server Error: {str(ex)}")
        }
