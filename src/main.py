import boto3
import requests
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SurfSpots')

OPENWEATHER_API_KEY = 'a136c0a529c69f6b7d6a97a873ed943a'

def get_weather_data(location):
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {}
    except requests.RequestException as e:
        print(f"Weather API request error: {str(e)}")
        return {}

def lambda_handler(event, context):
    try:
        # クエリパラメータが存在するかチェック
        location = event.get('queryStringParameters', {}).get('location')

        if not location:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing query parameter: location'})
            }

        # DynamoDBからスポット情報を検索するクエリ
        response = table.scan(
            FilterExpression="contains(#loc, :location)",
            ExpressionAttributeNames={
                "#loc": "location"
            },
            ExpressionAttributeValues={
                ":location": location
            }
        )

        spots = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps({'spots': spots})
        }

    except boto3.exceptions.Boto3Error as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'DynamoDB error: {str(e)}'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }
