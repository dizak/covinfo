#! /usr/bin/env bash

deploy(){
# $1 name of the cloud function
# $2 name of function from the main.py package to wrap as cloud function
# $3 amount of RAM to assign to the cloud function
    gcloud functions deploy "${1}"\
	--region=europe-west3\
	--trigger-http\
	--runtime=python37\
	--memory="${3}"\
	--source=./covinfo\
	--entry-point="${2}"\
	--allow-unauthenticated
}
