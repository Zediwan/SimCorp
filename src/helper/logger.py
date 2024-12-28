import logging
from tkinter import Text

class TextHandler(logging.Handler):
    def __init__(self, text_widget: Text):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.config(state='normal')
        self.text_widget.insert('end', msg + '\n')
        self.text_widget.config(state='disabled')
        self.text_widget.see('end')

class Logger:
    def __init__(self, name: str, text_widget: Text = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Check if the logger already has handlers to avoid adding multiple handlers
        if not self.logger.hasHandlers():

            # Create formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            if text_widget:
                th = TextHandler(text_widget)
                th.setFormatter(formatter)
                self.logger.addHandler(th)

    def get_logger(self):
        return self.logger

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)