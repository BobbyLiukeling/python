from scrapy.cmdline import execute

import sys
import os
import pdb


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "film"])