from loguru import logger

logger.add("debug.json", format="{time} {level} {message}",
level="DEBUG", rotation="30 KB", compression="zip", serialize=True)


logger.debug("Hello debug")
logger.info("Hello info")
logger.error("Hello error")










