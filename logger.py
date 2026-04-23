# Setup application logging system
import logging

# Configure logging to file with timestamp and level
def setup_logger():
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(message)s"
    )