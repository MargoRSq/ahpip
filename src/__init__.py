import os
import sys

if getattr(sys, 'frozen', False):
    static_dir = os.path.join(sys._MEIPASS, 'src/static')
else:
    static_dir = 'src/static'
