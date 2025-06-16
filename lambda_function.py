import os
import logging
import boto3
from keyword_auto_pipeline import run_pipeline

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SSM_PARAM_MAP = {
    'OPENAI_API_KEY': os.getenv('SSM_OPENAI_API_KEY', '/auto/openai/api_key'),
    'NOTION_API_TOKEN': os.getenv('SSM_NOTION_API_TOKEN', '/auto/notion/api_token'),
    'NOTION_HOOK_DB_ID': os.getenv('SSM_NOTION_HOOK_DB_ID', '/auto/notion/hook_db_id'),
    'NOTION_KPI_DB_ID': os.getenv('SSM_NOTION_KPI_DB_ID', '/auto/notion/kpi_db_id'),
}


def load_parameters():
    """Load sensitive parameters from AWS SSM if they are not provided as
    environment variables."""
    ssm = boto3.client('ssm')
    for env_key, param_name in SSM_PARAM_MAP.items():
        if os.getenv(env_key):
            continue
        try:
            value = ssm.get_parameter(Name=param_name, WithDecryption=True)['Parameter']['Value']
            os.environ[env_key] = value
            logger.info("Loaded %s from Parameter Store", env_key)
        except Exception as exc:
            logger.warning("Could not load %s from SSM: %s", env_key, exc)


def lambda_handler(event, context):
    load_parameters()
    run_pipeline()
    return {
        'statusCode': 200,
        'body': 'Pipeline executed successfully'
    }
