import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_request(response):
    """
    记录请求日志
    :param response: 请求响应对象
    """
    logger.info(f"Request URL: {response.url}")
    logger.info(f"Request Method: {response.request.method}")
    logger.info(f"Response Status Code: {response.status_code}")
