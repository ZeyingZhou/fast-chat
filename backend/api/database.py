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
        aws_access_key_id='local',  # Dummy credentials for local development
        aws_secret_access_key='local',
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
        # Conversations table 
        dynamodb.create_table(
            TableName='conversations',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'lastMessageAt', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'by-last-message',
                    'KeySchema': [
                        {'AttributeName': 'lastMessageAt', 'KeyType': 'HASH'}
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
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'conversationId', 'AttributeType': 'S'},
                {'AttributeName': 'createdAt', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'by-conversation',
                    'KeySchema': [
                        {'AttributeName': 'conversationId', 'KeyType': 'HASH'},
                        {'AttributeName': 'createdAt', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("Created messages table")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Messages table already exists")
        else:
            raise e
    try:
        # Messages table (with denormalized user data)
        dynamodb.create_table(
            TableName='conversation_users',
            KeySchema=[
                {'AttributeName': 'conversationId', 'KeyType': 'HASH'},
                {'AttributeName': 'userId', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'conversationId', 'AttributeType': 'S'},
                {'AttributeName': 'userId', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'by-user',
                    'KeySchema': [
                        {'AttributeName': 'userId', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("Created conversation_users table")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("conversation_users table already exists")
        else:
            raise e

# Helper functions for DynamoDB operations
def get_table(table_name: str):
    """Get a DynamoDB table by name"""
    return dynamodb.Table(table_name)

# Initialize tables on import
if __name__ == "__main__":
    create_tables()