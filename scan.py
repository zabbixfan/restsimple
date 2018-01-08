import socket
from multiprocessing.dummy import Pool
from concurrent import futures

import threading
p=4500
import logging
logging.basicConfig(level=logging.DEBUG,format='%(message)s')
def con(host):
    mutex=threading.Lock()
    # with mutex:
    port = 22
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(0.3)
    mutex.acquire()
    try:
        s.connect((host,port))
        #return "connect {}:{} success".format(host,port)
        return host
    except Exception as e:
        # print "{},{}".format(host,e)
        #logging.warn("{},{}".format(host,e))
        pass
    finally:
        mutex.release()
        s.close()
def scanport(port):
    # mutex=threading.Lock()
    # with mutex:
    port = port
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(0.3)
    # mutex.acquire()
    try:
        s.connect(('192.168.99.166',port))
        return "connect {} success".format(port)
    except Exception as e:
        print("{},{}".format(port,e))
        #logging.warn("{},{}".format(host,e))
        pass
    s.close()
    # mutex.release()
import time

l=[]
ip=["255","100","249"]
# ip=["100","2"]
ports=[i for i in range(1,60000)]
for i in ip:
    l.extend(["192.168.{}.{}".format(i,number) for number in range(0,255)])
def scan_many(func,args):
    pool = Pool(200)
    re = pool.map(func, args)
    pool.close()
    pool.join()
    return re
def scan_futrue(func,args):
    with futures.ProcessPoolExecutor(200) as executor:
        chunksize, extra = divmod(len(args),executor._max_workers*1)
        res = executor.map(func,args,chunksize=chunksize)
    return res
def main(func,args):
    t0=time.time()
    res = func(con,args)
    end = time.time()-t0
    # for i in res:
    #     if i:
    #         print i
    #return "res:{},time:{}".format([re for re in res if re],end)
    return [re+"\n" for re in res if re]

def main2(func,args):
    t0=time.time()
    res = func(scanport,args)
    end = time.time()-t0
    ps = []
    for re in res:
        if re:
            ps.append(re)
    for port in ps:
        print(port)
    return "res:{},time:{}".format(len(ps),end)
#hosts = main(func=scan_futrue,args=l)
#print len(hosts)
print(main2(func=scan_futrue,args=ports))


