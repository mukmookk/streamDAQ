import logging
import os
import datetime

# Set up logging
WD = os.environ.get('DAQWD') if os.environ.get('DAQWD') else os.getcwd()
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"{WD}/logs/crawl_{timestamp}.log"

logging.basicConfig(filename=filename, format='%(asctime)s %(levelname)s %(message)s')
logging.getLogger().setLevel(logging.INFO)