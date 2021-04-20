import aiohttp
from aiohttp_jinja2 import template
from proxylog import Session, ProxyLog


session = Session()


@template('index.html')
async def index(request):

    logs = session.query(ProxyLog).all()

    return {'logs':logs}


session.close()