import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='ap-south-1')  # Change region if needed

    # Fetch all running/stopped instances
    response = ec2.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running', 'stopped']}
        ]
    )

    auto_stop_ids = []
    auto_start_ids = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}

            stop_tag = tags.get('Minnath-Action-Stop', '')
            start_tag = tags.get('Minnath-Action-Start', '')

            if stop_tag == 'Minnath-Auto-Stop' and instance['State']['Name'] == 'running':
                auto_stop_ids.append(instance_id)
            elif start_tag == 'Minnath-Auto-Start' and instance['State']['Name'] == 'stopped':
                auto_start_ids.append(instance_id)

    if auto_stop_ids:
        ec2.stop_instances(InstanceIds=auto_stop_ids)
        print(f'Stopping instances: {auto_stop_ids}')
    else:
        print('No instances to stop.')

    if auto_start_ids:
        ec2.start_instances(InstanceIds=auto_start_ids)
        print(f'Starting instances: {auto_start_ids}')
    else:
        print('No instances to start.')

    return {
        'statusCode': 200,
        'body': 'Minnath-tagged EC2 instance automation executed successfully.'
    }

