# FastAPI-Lambda-Docker

## Project Description

### Deploying FastAPI on AWS Lambda using Docker

Project based off [Spacy Matcher](https://github.com/explosion/spacy-services), [Spacy Matcher demo UI](https://explosion.ai/demos/matcher). To be updated for spacy v3 API, refactored to use FastAPI.

Making use of relatively new feature of [Container Support for AWS Lambda](https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/)


### Running instructions

```bash
docker build -t matcher-service .

docker run -d --name matcher-service --rm -p 8000:80 matcher-service
```

Go to http://localhost:8000/docs for docs

## References

<https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/>

<https://explosion.ai/demos/matcher>

<https://github.com/explosion/spacy-services>

<https://towardsdatascience.com/fastapi-aws-robust-api-part-1-f67ae47390f9>

<https://medium.com/analytics-vidhya/python-fastapi-and-aws-lambda-container-3e524c586f01>

<https://youtu.be/6fE31084Uks?t=775>