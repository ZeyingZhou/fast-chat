# database.py
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()

def get_dynamodb():
    return boto3.resource(
        'dynamodb',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

dynamodb = get_dynamodb()

def create_tables():
    """Create DynamoDB tables matching messenger schema"""
    try:
        # Users table - Extended Clerk user info
        dynamodb.create_table(
            TableName='users',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}  # Clerk user ID
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
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
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
                {'AttributeName': 'lastMessageAt', 'AttributeType': 'S'},
                {'AttributeName': 'userId', 'AttributeType': 'S'}  # For querying user's conversations
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user-conversations-index',
                    'KeySchema': [
                        {'AttributeName': 'userId', 'KeyType': 'HASH'},
                        {'AttributeName': 'lastMessageAt', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Created conversations table")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Conversations table already exists")
        else:
            raise e

    try:
        # Messages table
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
                    'IndexName': 'conversation-messages-index',
                    'KeySchema': [
                        {'AttributeName': 'conversationId', 'KeyType': 'HASH'},
                        {'AttributeName': 'createdAt', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Created messages table")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Messages table already exists")
        else:
            raise e

# Example document structures:
example_user = {
    'id': 'clerk_user_id',  # From Clerk
    'email': 'user@example.com',  # From Clerk
    'name': 'User Name',
    'image': 'image_url',
    'conversationIds': ['conv1', 'conv2'],
    'seenMessageIds': ['msg1', 'msg2'],
    'createdAt': '2024-02-06T12:00:00Z',
    'updatedAt': '2024-02-06T12:00:00Z'
}

example_conversation = {
    'id': 'conv1',
    'name': 'Group Chat Name',
    'isGroup': True,
    'createdAt': '2024-02-06T12:00:00Z',
    'lastMessageAt': '2024-02-06T12:00:00Z',
    'userIds': ['user1', 'user2', 'user3'],
    'messageIds': ['msg1', 'msg2']
}

example_message = {
    'id': 'msg1',
    'body': 'Message content',
    'image': 'optional_image_url',
    'createdAt': '2024-02-06T12:00:00Z',
    'conversationId': 'conv1',
    'senderId': 'user1',
    'seenIds': ['user1', 'user2']
}

# Helper functions for DynamoDB operations
def get_table(table_name: str):
    """Get a DynamoDB table by name"""
    return dynamodb.Table(table_name)

# Initialize tables on import
if __name__ == "__main__":
    create_tables()