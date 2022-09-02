Deploy to Google Cloud
======================

From within the `cloud-function` directory execute the following statement:

```shell
gcloud functions deploy sentence-arithmetic-embeddings \
  --trigger-http \
  --gen2 \
  --serve-all-traffic-latest-revision \
  --region=asia-east2 \
  --allow-unauthenticated \
  --entry-point=classify_http \
  --memory=3GB \
  --max-instances=16 \
  --runtime=python39
```