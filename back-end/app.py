import aiohttp_jinja2
import jinja2
import aiohttp_autoreload
from aiohttp.web import Application, run_app, static
from config import get_configuration
from rest import RestResource
from models import Transaction

configuration = get_configuration()
app = Application()

# Static files
app.router.add_static('/static', path=configuration.DIST_DIR, name='static')

# REST API routes
transaction_resource = RestResource(
    'transactions',
    Transaction,
    ('id', 'board', 'value', 'weight'),
    'id',
    prefix='/api'
)
transaction_resource.register(app.router)

# Jinja2 setup
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(configuration.VIEWS_PATH))

# Main route
@aiohttp_jinja2.template(configuration.MAIN_VIEW)
async def index(request):
    return {}

app.router.add_get('/{tail:.*}', index, name='index')

if configuration.DEBUG:
    aiohttp_autoreload.start()

run_app(app)
