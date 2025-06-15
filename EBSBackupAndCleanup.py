import boto3
from datetime import datetime, timedelta

VOLUME_ID = 'vol-0b39fc2472f5e4cea'  # Replace with your volume ID
RETENTION_DAYS = 30

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Create a snapshot
    description = f"Automated snapshot for {VOLUME_ID} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    snapshot = ec2.create_snapshot(VolumeId=VOLUME_ID, Description=description)
    snapshot_id = snapshot['SnapshotId']
    print(f"Snapshot created: {snapshot_id}")

    # Tag snapshot
    ec2.create_tags(
        Resources=[snapshot_id],
        Tags=[
            {'Key': 'CreatedBy', 'Value': 'LambdaBackup'},
            {'Key': 'VolumeId', 'Value': VOLUME_ID}
        ]
    )

    # Cleanup old snapshots
    cutoff = datetime.utcnow() - timedelta(days=RETENTION_DAYS)

    snapshots = ec2.describe_snapshots(
        Filters=[
            {'Name': 'volume-id', 'Values': [VOLUME_ID]},
            {'Name': 'tag:CreatedBy', 'Values': ['LambdaBackup']}
        ],
        OwnerIds=['self']
    )

    for snap in snapshots['Snapshots']:
        if snap['StartTime'].replace(tzinfo=None) < cutoff:
            old_snap_id = snap['SnapshotId']
            ec2.delete_snapshot(SnapshotId=old_snap_id)
            print(f"Deleted old snapshot: {old_snap_id}")

    return {
        'statusCode': 200,
        'body': f"Snapshot {snapshot_id} created. Old snapshots deleted if older than {RETENTION_DAYS} days."
    }
