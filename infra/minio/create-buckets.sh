#!/bin/bash
# pod-ft MinIO bucket initialization
# schema-ref: project-schema.yaml#/databases/minio

MCLI_ALIAS=podft
MCLI_ENDPOINT=http://localhost:9000
MCLI_ACCESS_KEY=${MINIO_ACCESS_KEY:-podft-minio}
MCLI_SECRET_KEY=${MINIO_SECRET_KEY:-podft-minio-secret}

mc alias set $MCLI_ALIAS $MCLI_ENDPOINT $MCLI_ACCESS_KEY $MCLI_SECRET_KEY

BUCKETS=("raw-documents" "parsed-documents" "exports" "internal-documents")

for bucket in "${BUCKETS[@]}"; do
    if ! mc ls $MCLI_ALIAS/$bucket > /dev/null 2>&1; then
        mc mb $MCLI_ALIAS/$bucket
        echo "Created bucket: $bucket"
    else
        echo "Bucket already exists: $bucket"
    fi
done
