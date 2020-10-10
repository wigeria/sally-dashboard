""" Contains utilities for the sally bots """

from backend import settings
import boto3
from io import BytesIO
from selenium_yaml.parsers import YAMLParser


def parse_yaml_bot(yaml_string):
    """ Receives a YAML string as input and parses it as a valid bot

        Parameters
        ----------

        ``yaml_string`` : String; YAML File value

        Returns
        -------

        None; Raises a selenium_yaml.exceptions.ValidationError for any
            validation errors
    """
    parser = YAMLParser(yaml_string)
    parser.is_valid()


def create_s3_client():
    """ Returns a boto3.s3 client created using the AWS keys """
    client = boto3.client('s3',
        aws_access_key_id=settings.AWS_ACCESS,
        aws_secret_access_key=settings.AWS_SECRET
    )
    return client


def upload_bot(yaml_string, bot_path):
    """ Uploads the given yaml-string to the bot-path in the configured
        S3 bucket
    """
    s3_client = create_s3_client()
    fobj = BytesIO(yaml_string)
    # Upload the file
    response = s3_client.upload_fileobj(
        fobj, settings.AWS_BUCKET, bot_path)


def delete_bot(bot_path):
    """ Deletes the given bot path from S3 """
    s3_client = create_s3_client()
    s3_client.delete_object(Bucket=settings.AWS_BUCKET, Key=bot_path)


def download_bot(bot_path):
    """ Returns the contents of the file at the given path """
    s3_client = create_s3_client()
    inf = BytesIO()
    s3_client.download_fileobj(settings.AWS_BUCKET, bot_path, inf)
    inf.seek(0)
    return inf.getvalue()
