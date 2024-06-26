stage := "dev"
region := "us-east-1"

install:
    npm install
    poetry install

fmt:
    poetry run black app

test:
    PYTHONPATH=./ pytest -s

deploy:
    #!/usr/bin/env sh
    stage={{ stage }}
    region={{ region }}

    if [ "${stage}" != "dev" ] && [ "${stage}" != "production" ]; then
        echo "Stage must be 'dev' or 'production'"
        exit 1
    fi

    if [ "${stage}" == "production" ]; then

        while true; do
            read -p "Are you sure you want to deploy to production? " yn
            case $yn in
                [Yy]* ) break;;
                [Nn]* ) exit 1;;
                * ) echo "Please answer y or n";;
            esac
        done
    fi

    sls deploy --stage {{stage}} --region ${region} --verbose

start:
    sls offline
