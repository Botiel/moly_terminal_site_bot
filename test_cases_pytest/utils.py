import sys
import os
from datetime import datetime

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(CURR_DIR, '../')))
ROOT_DIR = sys.path[-1]

# CREATING TEST FOLDER PATH
FULL_TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
DATE_TIMESTAMP = datetime.now().strftime('%Y%m%d')
MAIN_FOLDER = f"{ROOT_DIR}/pytest_reports/{DATE_TIMESTAMP}"
