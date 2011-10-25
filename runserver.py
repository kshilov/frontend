import sys, os
cmd_folder = os.path.dirname(os.path.abspath("/home/iceberg/heymoose/heymoose"))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)

import __builtin__
__builtin__.DEBUG_CONFIG="/home/iceberg/heymoose/config_debug.py"
from heymoose import app
from heymoose.tests.gen_qa import generate_captcha

if __name__ == '__main__':
	generate_captcha()
	app.run(host="0.0.0.0",port=8989, debug=True)

