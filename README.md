# Serverless Airtable API

### Deploy

Before deploying:

1. Create a .env file locally from `.env.example`
2. Set `AIRTABLE_ACCESS_TOKEN` with a read+write Wildflower Airtable Personal Access Token
5. Deploy:


    just deploy

After initial deploy, add the Queue Event trigger to your S3 Bucket

### Development

Install pipenv and activate environment

    pipenv shell

Install serverless node environment (note this environment has shortcomings because of lack of SQS support)

    npm install
    just start

### Test

Run unit tests with a simple `justfile` command

    just test

### Production

    just stage=production deploy
