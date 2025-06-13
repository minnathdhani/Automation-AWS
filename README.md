# 🚀 Automated EC2 Instance Management using AWS Lambda and Boto3

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

### 2. IAM Role for Lambda

- Go to AWS IAM → Create a role for **Lambda**.
- Attach the following policy:
  - `AmazonEC2FullAccess` (for testing purposes; use custom least-privilege policy in production).
- Name the role: `LambdaEC2ManagerRole`.

---

## 🧠 Lambda Function

### Configuration:
- Runtime: **Python 3.x**
- Role: `LambdaEC2ManagerRole`
- Timeout: Recommended `1 minute`

### Lambda Code:


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

