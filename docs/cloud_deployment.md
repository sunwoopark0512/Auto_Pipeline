# Cloud Deployment Guide

This guide explains how to deploy and run the pipeline on AWS using EC2 Spot Instances and an Auto Scaling group. It also covers optional serverless approaches with AWS Lambda.

## Prerequisites

- An AWS account with permissions to create EC2, Auto Scaling, IAM, and Lambda resources.
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) installed and configured with your credentials.
- The repository cloned on an S3 bucket or AMI containing all required dependencies.

## Running on EC2 Spot Instances

1. **Create an IAM role** with permissions for EC2, Auto Scaling, CloudWatch, and S3 if you store artifacts there.
2. **Prepare a launch template** specifying the AMI, instance type, security groups, and user-data script to start `run_pipeline.py` on boot. See [`aws ec2 create-launch-template`](https://docs.aws.amazon.com/cli/latest/reference/ec2/create-launch-template.html).
3. **Create an Auto Scaling group** using the launch template and enable Spot Instances by setting a mixed instances policy. Example command:

   ```bash
   aws autoscaling create-auto-scaling-group \
     --auto-scaling-group-name my-pipeline-asg \
     --launch-template "LaunchTemplateName=my-pipeline-template,Version=1" \
     --mixed-instances-policy file://mixed-instances.json \
     --min-size 1 --max-size 10 --desired-capacity 1 \
     --region us-east-1
   ```

   Where `mixed-instances.json` configures Spot allocation and instance overrides. Refer to the [CLI documentation](https://docs.aws.amazon.com/cli/latest/reference/autoscaling/create-auto-scaling-group.html) for details.
4. **Define a scaling policy** if you want the pipeline to scale automatically, for example based on a schedule or a CloudWatch metric.
5. When instances launch, the user-data script should activate a Python environment and run `python run_pipeline.py`.

## Using AWS Lambda or Serverless Alternatives

For lightweight tasks or parts of the pipeline that can run independently, consider packaging them as AWS Lambda functions.

1. Write a handler that invokes the required script.
2. Create an execution role with necessary permissions.
3. Deploy the function with [`aws lambda create-function`](https://docs.aws.amazon.com/cli/latest/reference/lambda/create-function.html) and upload a zip package containing your code.
4. Use scheduled triggers via Amazon EventBridge to run the Lambda on a cron-like schedule.

Serverless options reduce management overhead but may require breaking the pipeline into smaller, stateless functions.

## Additional Resources

- [Auto Scaling documentation](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)
- [Spot Instance user guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html)
- [AWS Lambda documentation](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)

