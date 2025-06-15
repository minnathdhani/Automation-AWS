import boto3
import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Extract instance ID from the event
    instance_id = event['detail']['instance-id']
    
    # Generate current date
    current_date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    
    # Create tags
    tags = [
        {'Key': 'LaunchDate', 'Value': current_date},
        {'Key': 'Environment', 'Value': 'Auto-Tagged'}
    ]
    
    # Apply tags
    ec2.create_tags(Resources=[instance_id], Tags=tags)
    
    print(f"Tagged EC2 instance {instance_id} with: {tags}")

