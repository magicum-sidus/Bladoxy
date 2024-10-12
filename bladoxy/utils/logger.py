import logging

logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 设置日志格式
    handlers=[
        logging.StreamHandler()          # 输出到控制台
    ]
)



logger = logging.getLogger(__name__)



if __name__ == "__main__":
    logger.info("This is a log info")
    logger.debug("Debugging")
    logger.warning("Warning exists")
    logger.error("Error occurred")