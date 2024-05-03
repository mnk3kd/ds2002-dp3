import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/mnk3kd"
sqs = boto3.client('sqs')

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])


def get_messages(num_messages):
    try:
        # Receive messages from SQS queue. Each message has two MessageAttributes: order and word
        # You want to extract these two attributes to reassemble the message
        response = sqs.receive_message(
            QueueUrl=url,
            AttributeNames=['All'],
            MaxNumberOfMessages=num_messages,  # Specify the number of messages to retrieve
            MessageAttributeNames=['All']
        )
        # Check if there are messages in the queue
        if "Messages" in response:
            messages = []
            for message in response['Messages']:
                # Extract the message attributes you want to use as variables
                order = message['MessageAttributes']['order']['StringValue']
                word = message['MessageAttributes']['word']['StringValue']
                handle = message['ReceiptHandle']
                messages.append((order, word, handle))
            return messages
        else:
            print("No messages in the queue")
            return None
    except ClientError as e:
        print(e.response['Error']['Message'])

def your_function(num_of_iters):
    for i in range(num_of_iters):
        original_messages = get_messages(10)  # Assign the messages list
        if original_messages:
            # Remove the third element (handle) from each tuple and create new tuples with the remaining two elements
            
            modified_messages = []
            # Store the message data
            for order, word, handle in original_messages:
                modified_messages.append((order, word))
                delete_message(handle)
            
            # Reassemble the phrase
            words = [word for _, word in sorted(modified_messages, key=lambda x: int(x[0]))]
            phrase = ' '.join(words)
            print(f"Iteration {i+1} - Assembled Phrase:", phrase)


# Trigger the function
if __name__ == "__main__":
    your_function(10)  # Specify the number of iterations
  










#response = sqs.receive_message(
    #QueueUrl=url,
   #MaxNumberOfMessages=10  # Adjust as needed
#)

# Check if messages were received
#messages = response.get('Messages', [])
#if messages:
    #print("Messages received:")
    #for message in messages:
        #print(message)
#else:
    #print("No messages received.")