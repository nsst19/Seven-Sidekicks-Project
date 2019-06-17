#!/usr/local/bin/python3.6

import sys
import getopt 

from rest_api.general_application import app as g_app
from rest_api.music_application import app as m_app
from rest_api.video_application import app as v_app
from utilities.config_loader import load_config


def main(argv):
    cfg = load_config()

    type = ""

    try:
      opts, args = getopt.getopt(argv, "ht:", ["help", "type="])
    except getopt.GetoptError:
        print('__main__.py -t <api_type>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "help"):
            print('__main__.py -t <api_type>')
            sys.exit()
        elif opt in ('-t', "--type"):
            type = arg

    if type in ("general", ""):
        g_app.run(host=cfg['rest_api_host_url'], port=cfg['rest_api_host_port'], debug=False)
    elif type == "music":
        m_app.run(host=cfg['rest_api_host_url'], port=cfg['rest_api_host_port'], debug=False)
    elif type == "video":
        v_app.run(host=cfg['rest_api_host_url'], port=cfg['rest_api_host_port'], debug=False)


if __name__ == "__main__":
    main(sys.argv[1:])
