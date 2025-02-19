# database.py
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv(".env.local")

def get_dynamodb():
    return boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:8000',  # Point to local DynamoDB
        aws_access_key_id='dummy',  # Dummy credentials for local development
        aws_secret_access_key='dummy',
        region_name='us-east-1',
    )

dynamodb = get_dynamodb()

def create_tables():
    try:
        # Users table (keep as is since it's the source of truth for user data)
        dynamodb.create_table(
            TableName='users',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'email-index',
                    'KeySchema': [
                        {'AttributeName': 'email', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("Created users table")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Users table already exists")
        else:
            raise e
        
    try:
        # Conversations table (denormalized)
        dynamodb.create_table(
            TableName='conversations',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'userId', 'AttributeType': 'S'},
                {'AttributeName': 'lastMessageAt', 'AttributeType': 'S'},
                {'AttributeName': 'isGroup', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user-conversations-index',
                    'KeySchema': [
                        {'AttributeName': 'userId', 'KeyType': 'HASH'},
                        {'AttributeName': 'lastMessageAt', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                },
                {
                    'IndexName': 'user-direct-conversations-index',
                    'KeySchema': [
                        {'AttributeName': 'userId', 'KeyType': 'HASH'},
                        {'AttributeName': 'isGroup', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("Created conversations table")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Conversations table already exists")
        else:
            raise e
        
    try:
        # Messages table (with denormalized user data)
        dynamodb.create_table(
            TableName='messages',
            KeySchema=[
                {'AttributeName': 'conversationId', 'KeyType': 'HASH'},
                {'AttributeName': 'createdAt', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'conversationId', 'AttributeType': 'S'},
                {'AttributeName': 'createdAt', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("Created messages table")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Messages table already exists")
        else:
            raise e

# Helper functions for DynamoDB operations
def get_table(table_name: str):
    """Get a DynamoDB table by name"""
    return dynamodb.Table(table_name)

# Initialize tables on import
if __name__ == "__main__":
    create_tables()