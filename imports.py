import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse
import random
import time
from datetime import datetime
from tqdm import tqdm
import os
import asyncio
from curl_cffi.requests import AsyncSession
import tqdm
from urllib.parse import urlparse,parse_qs
import re
import sys
import subprocess
# Configuration
LINKS_DIR='Extracted_Links'
REPORTS_DIRECTORY = "Report_Downloads"
input_file='urls.txt'
date_part = datetime.now().strftime("%Y-%m-%d")

# 1. Configuration for Data pull from Online Excel File
