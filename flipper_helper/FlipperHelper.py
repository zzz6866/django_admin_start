from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


# IBK투자증권	0.0015	0.00518	제공
# 하나대투증권	0.0018		제공
# 동양증권	0.0020		제공
# 키움증권	0.0030	0.004864	제공
# 이베스트투자증권	0.0030		제공

# 단타 도우미 class
class FlipperHelper:
    def __init__(self):  # 초기화
        logger.info("INIT")

    @staticmethod
    def login():
        logger.info("LOG IN")

    @staticmethod
    def logout():
        logger.info("LOG OUT")
