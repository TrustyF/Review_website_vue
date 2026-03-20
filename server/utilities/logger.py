import logging
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)  # Set log level to DEBUG (can be changed to INFO, WARNING, etc.)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # This will log INFO and above to the console
logger.addHandler(console_handler)
