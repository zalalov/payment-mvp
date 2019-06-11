from flask import Flask, send_from_directory

from config import get_configuration

app = Flask(__name__)
configuration = get_configuration()
