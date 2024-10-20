from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class S3CommonParams:
    access_key = settings.S3_ACCESS_KEY
    secret_key = settings.S3_SECRET_KEY
    endpoint_url = settings.S3_ENDPOINT_URL
    gzip = True
    default_acl = "public-read"
    object_parameters = {"CacheControl": "max-age=86400"}


class StaticStorage(S3Boto3Storage, S3CommonParams):
    bucket_name = settings.S3_STATIC_BUCKET_NAME
    location = settings.S3_STATIC_LOCATION


class PublicMediaStorage(S3Boto3Storage, S3CommonParams):
    bucket_name = settings.S3_MEDIA_BUCKET_NAME
    location = settings.S3_MEDIA_LOCATION
