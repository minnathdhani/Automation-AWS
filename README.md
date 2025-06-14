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

Screenshorts:
1.

![Screenshot 2025-06-14 060915](https://github.com/user-attachments/assets/e8a88cca-605f-4810-a0f6-7c14c54c215d)<br>


2.

![Screenshot (9)](https://github.com/user-attachments/assets/5b04bfaf-3864-4e9a-ac48-73484b5d54c5)<br>
![Screenshot 2025-06-14 061011](https://github.com/user-attachments/assets/e442a7db-9912-4fe9-9974-aa8f90452ba1)<br>


3.


4.

![Screenshot 2025-06-14 061059](https://github.com/user-attachments/assets/93c80206-4a03-400d-8e22-9b3360fe2c63)<br>
![Screenshot 2025-06-14 061213](https://github.com/user-attachments/assets/845e85b1-afc0-4956-84b6-8f3f0f0579e1)<br>




5.
Before:
![Screenshot (11)](https://github.com/user-attachments/assets/96c22dba-defe-4d0f-9e1d-a6d76f43191b)<br>
After:
![Screenshot 2025-06-14 061316](https://github.com/user-attachments/assets/44c0c57e-4685-4612-9b95-ec6650525478)<br>
![Screenshot (12)](https://github.com/user-attachments/assets/48bbdb68-e81a-4594-9de6-7322fdbebb9c)<br>







