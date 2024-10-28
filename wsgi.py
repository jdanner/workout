import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from __init__ import app as application

if __name__ == "__main__":
    application.run()