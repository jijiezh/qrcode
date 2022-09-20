import os
import logging
logging_path = "/tmp"

if not os.path.exists(logging_path):
    os.mkdir(logging_path)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                    datefmt="%a, %d %b %Y %H:%M:%S",
                    filename=os.path.join(logging_path, "send_qywx_msg.log"),
                    filemode='a')
