import logging
import datetime
import time
import numpy as np

VERBOSE = 1  # Set to 1 for debugging info

name = 'output/imagetest'  # name prefix used to create all outputs
logfile = name + '.log'  # log output will be directed to this file and to screen

nrays = 1_000_000
xmax = 25.

beam = {
    'x': 0.,
    'y': 0.
}

light = {
    0: 'OTR',
    1: 'F1',
    2: 'F2',
    3: 'F3',
    4: 'Laser'
}

light_source = 0

foil = {
    'ID': 1,
    'normal': np.array([[0, -1, 0]]),
    'diam': 50.  # 55.0, original C++ code, not sure why
}

M0 = {
    'name': 'PlaneMirror',
    'normal': np.array([[0., 0., -1.]]),
    'R': 15.,
    'X': np.array([[0., 0., 10.]]),
    'angles': np.zeros(3)
}

mirror1 = {
    'x': 1.,
    'y': 2.,
    'f': 3.
}

mirror2 = {
    'x': 4.,
    'y': 5.,
    'f': 6.
}

mirror3 = {
    'x': 7.,
    'y': 8.,
    'f': 9.
}

mirror4 = {
    'x': 10.,
    'y': 11.,
    'f': 12.
}

mirrors = [mirror1, mirror2, mirror3, mirror4]

camera = {
    'npxlX': 484,
    'npxlY': 704,
    'focal distance': 60.
}

level = logging.DEBUG if VERBOSE else logging.INFO
# message = '%(levelname)s:%(name)s: %(message)s\n'
# message = '%(levelname)s: %(message)s\n'
message = '%(message)s\n'
logging.basicConfig(filename=logfile, filemode='w', format=message)
logger = logging.getLogger('pyOTR')
logger.setLevel(level)
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(logfile)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def GetTime(start=True):
    now = datetime.datetime.now()
    now = now.strftime('%Y, %b %d %H:%M:%S')
    if start:
        message = f'{now}\nStarting pyOTR:'
    else:
        message = f'Ending pyOTR, bye!!\n{now}'
    logger.info(message)


# Decorator to measure the time each function takes to run:
def timer(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        dt = time.time() - t0
        logger.info(f'{func.__name__} ran in {dt:.2f} s')
        return result
    return wrapper
