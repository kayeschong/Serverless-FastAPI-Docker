# Serverless-FastAPI-Docker

## Project Description

### Deploying FastAPI on Serverless Platforms using Docker

Project based off [Spacy Matcher](https://github.com/explosion/spacy-services), [Spacy Matcher demo UI](https://explosion.ai/demos/matcher). To be updated for spacy v3 API, refactored to use FastAPI.

AWS added [Container Support for AWS Lambda](https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/) near the end of 2020, while GCP has [Cloud Run](https://cloud.google.com/run).

## Running locally

```bash
docker build -t matcher-service-dev .

docker run -d --name matcher-service --rm -p 8000:80 matcher-service
```

Go to http://localhost:8000/docs for docs


## Deploy to AWS Lambda

1. Create an [IAM user](https://console.aws.amazon.com/iam/home#/users) with access to Lambda, ECR, S3 and API gateway.

2. Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) and [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) for your respective OS. Then, [configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) with your credentials. 

    For example, place credentials in local .env file, and load into environment session:

    ```bash
    export PROJECT_NAME=matcher-service
    export $(cat .env | xargs)
    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
    aws configure set region $AWS_REGION
    aws configure set output $AWS_OUTPUT
    ```

3. Using SAM CLI to deploy to AWS Lambda

    First time setup
    ```bash
    # Login to ECR with credentials
    aws ecr get-login-password | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

    # Create container repository if not already available
    aws ecr create-repository --repository-name mini-projects-repo --image-tag-mutability IMMUTABLE --image-scanning-configuration scanOnPush=true

    sam build --template-file template-prod.yml
    sam validate --template-file .aws-sam/build/template.yaml
    
    sam package --output-template-file packaged.yaml --image-repositories MatcherFunction=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/mini-projects-repo

    sam deploy --template-file packaged.yaml --stack-name matcher-service --capabilities CAPABILITY_IAM --image-repositories MatcherFunction=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/mini-projects-repo --region ${AWS_REGION} --no-confirm-changeset
    ```

    Subsequent deploys
    ```bash
    # Set environment variables/credentials

    sam build --template-file template-prod.yml

    sam validate --template-file .aws-sam/build/template.yaml
    
    sam package --output-template-file packaged.yaml --image-repositories MatcherFunction=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/mini-projects-repo

    sam deploy --template-file packaged.yaml --stack-name matcher-service --capabilities CAPABILITY_IAM --image-repositories MatcherFunction=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/mini-projects-repo --region ${AWS_REGION} --no-confirm-changeset
    ```

4.  CI/CD with github actions

## Deploy to GCP Cloud Run
~In Progress~

## Pricing links
<https://aws.amazon.com/lambda/pricing/>

<https://aws.amazon.com/ecr/pricing/>

## References

<https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/>

<https://aws.amazon.com/blogs/compute/using-container-image-support-for-aws-lambda-with-aws-sam/>

<https://docs.aws.amazon.com/lambda/latest/dg/lambda-images.html>

<https://explosion.ai/demos/matcher>

<https://github.com/explosion/spacy-services>

<https://towardsdatascience.com/fastapi-aws-robust-api-part-1-f67ae47390f9>

<https://medium.com/analytics-vidhya/python-fastapi-and-aws-lambda-container-3e524c586f01>

<https://iwpnd.pw/articles/2020-01/deploy-fastapi-to-aws-lambda>

<https://youtu.be/6fE31084Uks?t=775>
