from app import app
from views.common import *
from views.user import *
from views.transaction import *
from models import *
from initial import *


if __name__ == '__main__':
    app.run()
