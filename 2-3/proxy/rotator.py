
from itertools import cycle, count
import time
from datetime import datetime, timedelta
from proxylog import Session, ProxyLog
import asyncio, requests, csv


proxy = set()


with open("assets/proxy.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        proxy.add(line.strip())


proxies = list(proxy)
proxy_pool = cycle(proxies)



f = open("assets/ascii.txt", "r")
clock = f.read()

session = Session()


async def snmp():
    while True:
    
        proxy = next(proxy_pool)
    

        now = datetime.now()
        t = now.strftime("%D - %H:%M:%S")

        proxylog =  ProxyLog()
        proxylog.proxy_address = proxy

        proxylog.online = now

        session.add(proxylog)
        session.commit()
        timeout = 120
        print( f'{t} \nSuccessfully connected to {proxy} \nChanging in {timeout} seconds \nproxy dead, proceeding to a new one...' )



        await asyncio.sleep(timeout)

        of = datetime.now()
        proxylog.offline = of

        session.commit()

        print( f'{t}\n{proxy}  is offline after {timeout} seconds! ', kmsg)



async def proxy():
    while True:
        now = datetime.now()

        t = now.replace(day=now.day, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        w = t - now
        print(f' Time:{now} \n Scheduled upload:{t} \n Until Scheduled Upload: {w} ')


        await asyncio.sleep(w.total_seconds())

        
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(days=1)

        results = session.query(ProxyLog).filter(ProxyLog.online >= yesterday).filter(ProxyLog.online <= today)
        

        filename = datetime.now().strftime('%m%d0%Y%H%M%S')

        with open(f'{filename}result.csv', 'w') as file:

            writer = csv.writer(file, delimiter = '\t', lineterminator = '\n',)
            writer.writerow(['IP','ONLINE','OFFLINE'])

            for result in results:

                writer.writerow([result.proxy_address,result.online,result.offline])
            

        url ='http://127.0.0.1:5000/'
        r = requests.post(url, files={'file': (f'{filename}result.csv', open(f'{filename}result.csv', 'rb'))})
        




loop = asyncio.get_event_loop()
loop.create_task(snmp())
loop.create_task(proxy())
loop.run_forever()

session.close()