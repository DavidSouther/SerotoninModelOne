#!/bin/sh

alias gcloud=./google-cloud-sdk/bin/gcloud

# Connect kubctl to cluster
gcloud container clusters get-credentials serotonin-cluster --zone=us-central1-c

# Prepare the image
IMAGE=gcr.io/southerd/serotonin:alpha1
gcloud builds submit --tag $IMAGE

# Run the image for each flag
for F in $(ls flags) ; do 
    FLAGS=${F#flags.}
    POD=$(echo serotonin-${FLAGS//[^-a-zA-Z0-9]/-} | tr '[:upper:]' '[:lower:]')
    kubectl delete pod $POD
    kubectl run $POD \
        --image=$IMAGE \
        --replicas=1 \
        --restart="Never" \
        --env="PARAMS=$FLAGS" \
        --env="SERVICE_AGENT_PASSPHRASE=${SERVICE_AGENT_PASSPHRASE}"
done
