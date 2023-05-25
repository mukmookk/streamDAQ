import logging
import os
import datetime

# Set up logging
WD = os.environ.get('DAQWD') if os.environ.get('DAQWD') else os.getcwd()
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"{WD}/logs/crawl_{timestamp}.log"
log_dir = os.path.join(WD, 'logs')
os.makedirs(log_dir, exist_ok=True)

try:
    logging.basicConfig(filename=filename, format='%(asctime)s %(levelname)s %(message)s')
    logging.getLogger().setLevel(logging.INFO)
except:
    log_dir = os.path.join(WD, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(filename=filename, format='%(asctime)s %(levelname)s %(message)s')
    logging.getLogger().setLevel(logging.INFO)