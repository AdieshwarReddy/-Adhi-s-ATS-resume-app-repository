import os
import sys

# Ensure repository root and frontend are on Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from frontend.streamlit_app import main

if __name__ == "__main__":
    main()

