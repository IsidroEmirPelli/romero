from subprocess import Popen
from sys import argv
from os import kill
from signal import CTRL_BREAK_EVENT
from PyQt5.Qt import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication


def start_django():
    django_server = Popen(['python', 'manage.py', 'runserver'], shell=True)
    return django_server


def generate_browser():
    app = QApplication(argv)
    app.setApplicationName("Base de datos - Romero")
    web = QWebEngineView()
    web.load(QUrl("http://127.0.0.1:8000"))
    web.showMaximized()
    app.exec_()  # This is the main loop of the application.


if __name__ == '__main__':
    django_server = start_django()  # Start django server and get the process id
    generate_browser()
    try:
        kill(django_server.pid, CTRL_BREAK_EVENT)
    except:
        django_server.terminate()
