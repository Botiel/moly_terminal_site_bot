import sys
from os.path import dirname, abspath
from datetime import datetime

d = dirname(dirname(abspath(__file__)))
sys.path.append(d)
ROOT_DIR = sys.path[-1]

# CREATING TEST FOLDER
FULL_TIMESTAMP = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
DATE_TIMESTAMP = datetime.now().strftime('%d-%m-%Y')
MAIN_FOLDER = f"{ROOT_DIR}/pytest_reports/{DATE_TIMESTAMP}"

