'''
(*)~----------------------------------------------------------------------------------
 Pupil - eye tracking platform
 Copyright (C) 2012-2016  Pupil Labs

 Distributed under the terms of the GNU Lesser General Public License (LGPL v3.0).
 License details are in the file license.txt, distributed as part of this software.
----------------------------------------------------------------------------------~(*)
'''
import os
from pyglui import ui
from plugin import Plugin

#logging
import logging
logger = logging.getLogger(__name__)

class Log_to_Callback(logging.Handler):
    def __init__(self,cb):
        super(Log_to_Callback, self).__init__()
        self.cb = cb

    def emit(self,record):
        self.cb(record)

class Log_History(Plugin):
    """Simple logging GUI that displays the last N messages from the logger"""
    def __init__(self, g_pool):
        super(Log_History, self).__init__(g_pool)
        self.menu = None
        self.num_messages = 50

    def init_gui(self):

        def close():
            self.alive = False

        help_str = "This menu shows the last %s messages from the logger. See world.log or eye.log files for full logs." %(self.num_messages)
        self.menu = ui.Scrolling_Menu('Log')
        self.g_pool.gui.append(self.menu)
        self.menu.append(ui.Button('Close',close))
        self.menu.append(ui.Info_Text(help_str))

        self.log_handler = Log_to_Callback(self.on_log)
        logger = logging.getLogger()
        logger.addHandler(self.log_handler)
        self.log_handler.setLevel(logging.INFO)

    def on_log(self,record):
        self.menu.elements[self.num_messages+2:] = []
        self.menu.insert(2,ui.Info_Text("%s - %s" %(record.levelname, record.msg)))


    def deinit_gui(self):
        if self.menu:
            logger = logging.getLogger()
            logger.removeHandler(self.log_handler)
            self.g_pool.gui.remove(self.menu)
            self.menu= None

    def cleanup(self):
        self.deinit_gui()

    def get_init_dict(self):
        return {}