#! /usr/bin/env bash

gcloud functions deploy covinfo\
    --region=europe-west3\
    --trigger-http\
    --runtime=python37\
    --memory=128MB\
    --source=./covinfo\
    --entry-point=get_daily_data\
    --allow-unauthenticated
