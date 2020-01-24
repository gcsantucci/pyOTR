import logging
import datetime
import numpy as np

VERBOSE = 0  # Set to 1 for debugging info.

logfile = 'otr_sim.log'

nrays = 100_000
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
    'ID':     1,
    'normal': np.array([[0, 1, 0]]),
    'diam':   50.  # 55.0, original C++ code, not sure why
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
    'npxlX':    484,
    'npxlY':    704,
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

logger.info(datetime.time())
logger.info('Starting pyOTR!')
