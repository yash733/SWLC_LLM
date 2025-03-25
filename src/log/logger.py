import logging

logging.basicConfig(
    level= logging.DEBUG,
    format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode= 'w',
    filename= './src/log/.log'
)