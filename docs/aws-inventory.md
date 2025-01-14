# AWS Inventory YAML

## Secrets Configuration

### 1. Adding Secrets to GitHub Repository
Secrets are encrypted environment variables that GitHub Actions can use during workflow execution.

**Steps to Add Secrets:**
1. Navigate to your GitHub repository.
2. Click on **Settings** (top-right corner of the repository interface).
3. In the left sidebar, under **Security**, click **Secrets and variables**, then select **Actions**.
4. Click the **New repository secret** button.
5. Add the following secrets:
   - **Name:** `AUTOMATION_AWS_ACCESS_KEY_ID`
     - **Value:** Your AWS Access Key ID.
   - **Name:** `AUTOMATION_AWS_SECRET_ACCESS_KEY`
     - **Value:** Your AWS Secret Access Key.

These keys must have the necessary permissions to list and describe AWS resources for inventory purposes. Typically, the associated IAM user or role should have the following AWS policies:
- `ReadOnlyAccess` policy (ensures it only fetches data and does not modify resources).
- Additional custom permissions if your workflow requires fetching specific resource types not covered by `ReadOnlyAccess`.

### 2. Verifying Permissions
Ensure the IAM credentials have proper permissions:
- Verify the access keys belong to a secure IAM user or role.
- Use AWS policy simulators or tools to confirm the assigned policies.

**Minimal Required Permissions Example:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "s3:ListAllMyBuckets",
        "rds:Describe*",
        "iam:List*",
        "cloudformation:Describe*"
      ],
      "Resource": "*"
    }
  ]
}
```

### 3. Managing Secrets Safely
- Rotate secrets regularly and revoke unused credentials.
- Avoid hardcoding secrets in your workflow or repository files to reduce the risk of accidental exposure.

---

