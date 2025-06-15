# 🚀 1. Automated EC2 Instance Management using AWS Lambda and Boto3

## 📘 Overview

This project automates the **start and stop** of EC2 instances based on **custom tag values** using **AWS Lambda** and **Boto3** (AWS SDK for Python). This automation helps manage compute resources efficiently without manual intervention.

---

## 🎯 Objective

To create an AWS Lambda function that:
- **Stops** EC2 instances tagged with `Minnath-Action-Stop = Minnath-Auto-Stop`
- **Starts** EC2 instances tagged with `Minnath-Action-Start = Minnath-Auto-Start`

---

## 🏗️ Project Setup

### 1. EC2 Instance Setup

- Launch two EC2 instances (`t2.micro` or free-tier eligible).
- Tag them as follows:
  - **Instance 1 (to stop)**:
    - Key: `Minnath-Action-Stop`
    - Value: `Minnath-Auto-Stop`
  - **Instance 2 (to start)**:
    - Key: `Minnath-Action-Start`
    - Value: `Minnath-Auto-Start`
   
   
![Screenshot 2025-06-14 060915](https://github.com/user-attachments/assets/e8a88cca-605f-4810-a0f6-7c14c54c215d)<br>

---

### 2. IAM Role for Lambda

- Go to AWS IAM → Create a role for **Lambda**.
- Attach the following policy:
  - `AmazonEC2FullAccess` (for testing purposes; use custom least-privilege policy in production).
- Name the role: `LambdaEC2ManagerRole`.

![Screenshot (21)](https://github.com/user-attachments/assets/71e29787-9e01-4406-9057-7f4027416f1b)<br>


---

## 🧠 Lambda Function

### Configuration:
- Runtime: **Python 3.x**
- Role: `LambdaEC2ManagerRole`
- Timeout: Recommended `1 minute`
  
![Screenshot (9)](https://github.com/user-attachments/assets/5b04bfaf-3864-4e9a-ac48-73484b5d54c5)<br>
![Screenshot 2025-06-14 061011](https://github.com/user-attachments/assets/e442a7db-9912-4fe9-9974-aa8f90452ba1)<br>

---

### Lambda Code:

```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='us-east-1')  # Change region if needed

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

```

---

## 🔬 Testing

To test the Lambda function manually:

1. Go to the **Lambda console** in AWS.
2. Click **Test** at the top of the function editor.
3. Use the default test event:  
   ```json
   {}
4.Navigate to the EC2 Dashboard and verify:
- Instances tagged with Minnath-Auto-Stop should be stopped.
- Instances tagged with Minnath-Auto-Start should be started.

---

## Screenshorts:

![Screenshot 2025-06-14 061059](https://github.com/user-attachments/assets/93c80206-4a03-400d-8e22-9b3360fe2c63)<br>
![Screenshot 2025-06-14 061213](https://github.com/user-attachments/assets/845e85b1-afc0-4956-84b6-8f3f0f0579e1)<br>

### Before:
![Screenshot (11)](https://github.com/user-attachments/assets/96c22dba-defe-4d0f-9e1d-a6d76f43191b)<br>
![Screenshot 2025-06-14 060915](https://github.com/user-attachments/assets/e8a88cca-605f-4810-a0f6-7c14c54c215d)<br>

## After:
![Screenshot 2025-06-14 061316](https://github.com/user-attachments/assets/44c0c57e-4685-4612-9b95-ec6650525478)<br>
![Screenshot (12)](https://github.com/user-attachments/assets/48bbdb68-e81a-4594-9de6-7322fdbebb9c)<br>



-----

# 🧹 2. Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

## 📌 Objective

Automate the deletion of files older than 30 days in an S3 bucket using AWS Lambda and Boto3.  
Since we cannot backdate S3 object timestamps directly, this project uses **filename-based date logic** for testing.

---

## 🧱 Components Used

- AWS S3
- AWS Lambda (Python 3.x)
- AWS IAM (Role and Policy)
- AWS CloudWatch (for logs)
- Boto3 (Python SDK for AWS)

---

## 🛠️ Setup Instructions

### 1. 🚀 Create an S3 Bucket

1. Go to the AWS Console → **S3**
2. Click **Create bucket**
3. Name it something like: `s3-lambda-cleanup-demo`
4. Keep default settings or customize as needed
5. Upload the following sample files with **date in filename**:

report_2024-04-01.txt <-- simulate OLD
report_2025-04-13.txt <-- simulate OLD
report_2025-06-15.txt <-- recent

>>> ⚠️ Note: AWS doesn’t allow backdating `LastModified`. Instead, we use the filename to simulate age.

<img width="949" alt="image" src="https://github.com/user-attachments/assets/5a2c13d1-c8a6-413d-9d4b-2bb506ee666d" /><br>


---

### 2. 🛡️ Create IAM Role for Lambda

1. Go to AWS Console → **IAM** → Roles → **Create role**
2. **Trusted entity**: Select `Lambda`
3. **Permissions**: Attach policy `AmazonS3FullAccess`
4. Click **Next** → Add a role name: `LambdaS3CleanupRole`
5. Click **Create Role**

<img width="944" alt="image" src="https://github.com/user-attachments/assets/2c00af0b-4f6d-45be-8a2b-0ada59faff11" /><br>


---

### 3. 🧠 Create Lambda Function

1. Go to AWS Console → **Lambda**
2. Click **Create function**
3. Set:
- Name: `S3CleanupFunction`
- Runtime: `Python 3.12` (or latest)
- Permissions: Use **existing role** `LambdaS3CleanupRole`
4. Click **Create function**

<img width="944" alt="image" src="https://github.com/user-attachments/assets/5334450a-c091-41b4-85bd-b2f6c6ad9cb1" /><br>


---

### 4. 🧾 Lambda Code (Filename-based Cleanup)

Replace default code with the following:

```python
import boto3
import datetime
import re
import os

s3 = boto3.client('s3')

# Customize bucket name and days threshold
BUCKET_NAME = 's3-lambda-cleanup-demo'
DAYS_THRESHOLD = 30

def extract_date_from_filename(filename):
 """Extract YYYY-MM-DD from the filename using regex"""
 match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
 if match:
     try:
         return datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
     except ValueError:
         return None
 return None

def lambda_handler(event, context):
 try:
     response = s3.list_objects_v2(Bucket=BUCKET_NAME)
     if 'Contents' not in response:
         print("Bucket is empty.")
         return

     today = datetime.date.today()
     deleted_files = []

     for obj in response['Contents']:
         key = obj['Key']
         file_date = extract_date_from_filename(key)

         if not file_date:
             print(f"Skipping file without valid date: {key}")
             continue

         age = (today - file_date).days

         if age > DAYS_THRESHOLD:
             print(f"Deleting old file: {key} (Age: {age} days)")
             s3.delete_object(Bucket=BUCKET_NAME, Key=key)
             deleted_files.append(key)
         else:
             print(f"Keeping file: {key} (Age: {age} days)")

     print(f"✅ Deleted {len(deleted_files)} file(s): {deleted_files}")

 except Exception as e:
     print(f"❌ Error: {str(e)}")
```

---

### 5. 🧪 Test the Function

From Lambda Console → Click Test
Create a test event (can leave it empty)
Click Test

![Screenshot (22)](https://github.com/user-attachments/assets/26c2f6d3-8e4a-4e7c-a7bd-d0191f258ba4)<br>


----

 ### Cleanup
Delete the Lambda function (optional)
Delete the IAM role (optional)
Delete the S3 bucket if no longer needed\

---

### 📎 Notes
In real-world usage, rely on LastModified from S3 metadata instead of filenames.
For secure implementation, use least privilege IAM policy rather than AmazonS3FullAccess.

---

### 📚 References
Boto3 S3 Docs
AWS Lambda Docs
IAM Best Practices


---


# 📦 4.Automated EBS Snapshot Creation and Cleanup using AWS Lambda & Boto3

## 📌 Objective

This project automates the process of creating Amazon EBS snapshots and cleaning up snapshots older than a specified retention period (e.g., 30 days) to optimize backup management and reduce storage costs.

---

## ✅ Features

- Automated snapshot creation for specified EBS volumes.
- Automatic deletion of snapshots older than a defined retention period.
- Optional tagging for easier snapshot identification.
- Scheduled execution using Amazon EventBridge (CloudWatch Events).

---

## 🛠️ Prerequisites

- AWS Account with sufficient permissions.
- At least one EBS volume attached or available.
- Basic understanding of AWS services: EC2, IAM, Lambda, and EventBridge.
- Python 3.x (Lambda runtime support).

---

## 🔧 Setup Instructions

### 1. EBS Volume Preparation

1. Navigate to the **EC2 Dashboard** → **Elastic Block Store** → **Volumes**.
2. Create or identify an existing EBS volume.
3. **Note down the Volume ID** (e.g., `vol-0a1b2c3d4e5f67890`).


![Screenshot 2025-06-15 003948](https://github.com/user-attachments/assets/2265b602-83f6-40d0-8e80-dd01098ae491)<br>


---

### 2. IAM Role for Lambda

1. Go to **IAM** → **Roles** → **Create Role**.
2. Select **Lambda** as the trusted entity.
3. Attach the **`AmazonEC2FullAccess`** policy (for demonstration purposes).
   > ⚠️ In production, use a restrictive policy (see Appendix below).
4. Name the role (e.g., `LambdaEBSBackupRole`) and create it.

![Screenshot (15)](https://github.com/user-attachments/assets/c2672315-f493-4a68-ac1f-9310b7db30ef)<br>

---

### 3. Lambda Function Setup

1. Go to **AWS Lambda** → **Create Function**.
2. Enter:
   - **Function name**: `EBSBackupFunction`
   - **Runtime**: Python 3.12
   - **Permissions**: Use the existing role `LambdaEBSBackupRole`
3. Click **Create Function**.

![Screenshot (17)](https://github.com/user-attachments/assets/59c542b7-6067-436e-b9ba-2543305993a2)<br>


---

### 4. Add Lambda Function Code

Replace the default code with the following:

```python
import boto3
from datetime import datetime, timedelta

VOLUME_ID = 'vol-0a1b2c3d4e5f67890'  # Replace with your actual volume ID
RETENTION_DAYS = 30

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Create snapshot
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

    # Delete old snapshots
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
            ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])
            print(f"Deleted old snapshot: {snap['SnapshotId']}")

    return {
        'statusCode': 200,
        'body': f"Snapshot {snapshot_id} created. Old snapshots deleted if older than {RETENTION_DAYS} days."
    }

```
-----
4. Click Deploy.

   ![Screenshot (14)](https://github.com/user-attachments/assets/343c7039-1dd7-4d32-ab7f-b9b942012411)<br>


---

### 5. Test the Lambda Function:
1. Click Test
  Configure a new test event (use any name, e.g., TestBackupEvent)
  Payload: {} (leave default)
  Click Test

2. Check Output:
In the Log Output, you should see:

Snapshot created: snap-xxxxxxxxxxxxx
Deleted old snapshot: snap-yyyyyyyyyyyy (if any old ones exist)

3. Go to EC2 → Snapshots
Confirm the new snapshot exists
Check the Tags tab → You should see CreatedBy: LambdaBackup


![Screenshot (13)](https://github.com/user-attachments/assets/46f9a0b4-3c6d-4d65-ba0b-59a3065c0bf1)<br>
![Screenshot (19)](https://github.com/user-attachments/assets/5960c6ee-4b77-4dd0-b9f3-9e40660ea943)<br>
![Screenshot (20)](https://github.com/user-attachments/assets/c149b6ca-dfe1-45d8-b7ef-0bbff1bc35c0)<br>


------

# 🏷️ EC2 Auto-Tagging via AWS Lambda & EventBridge

This project implements an **automated EC2 instance tagging solution** using AWS Lambda and EventBridge. Whenever a new EC2 instance changes to the `running` state, this system applies predefined tags such as `LaunchDate` and `Environment` to the instance automatically.

---

## 📌 Objective

To streamline infrastructure management by:
- Automatically tagging EC2 instances upon launch.
- Reducing manual effort and ensuring consistent metadata across resources.

---

## 🚀 Architecture Overview

1. **Event Source**:  
   AWS EventBridge listens for EC2 state change events.

2. **Trigger Condition**:  
   When an EC2 instance transitions to the `running` state, EventBridge triggers a Lambda function.

3. **Lambda Function**:  
   - Extracts the `instance-id` from the event.
   - Applies two tags to the instance:
     - `LaunchDate`: Current UTC date
     - `Environment`: `Auto-Tagged`

---

## 🧠 How It Works

### Example EventBridge Event (Trigger Payload)
```json
{
  "detail-type": "EC2 Instance State-change Notification",
  "source": "aws.ec2",
  "detail": {
    "instance-id": "i-0987792ea6f440667",
    "state": "running"
  }
}
```

### Lambda Function Behavior
- Validates the presence of `detail` and `instance-id`.
- Tags the instance using `boto3` EC2 client.
- Handles errors gracefully and logs complete event data for debugging.

---

## 🧾 Prerequisites

- AWS account with permissions to:
  - Create/manage Lambda functions
  - Read EC2 events
  - Tag EC2 resources
- IAM Role for Lambda with the following policy permissions:
  - `ec2:CreateTags`
  - `logs:*`
- Python 3.9+ runtime (used in Lambda)

---

## 📂 Project Structure

```
ec2-auto-tagging/
├── lambda_function.py      # Main Lambda code
├── README.md               # Documentation
```

---

## 🛠️ Deployment Steps

### Step 1: Create the Lambda Function

1. Go to AWS Lambda console.
2. Create a new Lambda function with:
   - Runtime: Python 3.9 or later
   - Execution Role: With EC2 tag permissions
3. Paste the code from `lambda_function.py`.

   
    ### EC2 Instance pic
   <img width="947" alt="image" src="https://github.com/user-attachments/assets/ef9935aa-a491-4ce4-98d0-0cd342466015" /><br>
    ### IAM Roles for Auto-tagging
    <img width="947" alt="image" src="https://github.com/user-attachments/assets/4622524d-2a8d-45cc-981c-44e27c42b5a8" /><br>
    ### Creation of Lambda Function
   <img width="949" alt="image" src="https://github.com/user-attachments/assets/efb683fd-cc58-4c50-8663-3fa7f51919b6" /><br>
   
---
   
### Step 2: Configure EventBridge Rule

1. Navigate to **Amazon EventBridge > Rules > Create Rule**
2. Define a name like `TagEC2OnLaunch`
3. Event pattern:
   ```json
   {
     "source": ["aws.ec2"],
     "detail-type": ["EC2 Instance State-change Notification"],
     "detail": {
       "state": ["running"]
     }
   }
   ```
4. Set target as the Lambda function.

### EventBridge Rule
<img width="945" alt="image" src="https://github.com/user-attachments/assets/1c8bb5de-adef-4593-91b1-53fcb367801c" /><br>


---

## ✅ Expected Output

Once configured, whenever a new EC2 instance enters the `running` state, your Lambda function will:

- Automatically tag the instance with the launch date and environment.
- Log tagging confirmation in CloudWatch.

Example:
```
✅ Tagged EC2 instance i-0987792ea6f440667 with: [{'Key': 'LaunchDate', 'Value': '2025-06-15'}, {'Key': 'Environment', 'Value': 'Auto-Tagged'}]
```

### Final Output pic
![Screenshot (23)](https://github.com/user-attachments/assets/b434370f-3e54-43d7-8317-d02a68ec570c)<br>


---

## 🧪 Testing

You can test this by:
- Manually launching a new EC2 instance.
- Or using the Lambda test console with a sample event payload.

---

## 📎 Notes

- This solution is extensible to include additional tags or trigger conditions.
- Be sure to monitor CloudWatch Logs for any unexpected errors.

---

## 📧 Contact

For any questions or improvements, feel free to reach out or contribute to the project.







