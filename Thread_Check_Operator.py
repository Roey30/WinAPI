"""
Name : Roey Firan
Program name : Data_Base WinAPI
Date : 24/12/2022
Description: Uses to sync the data_base using threads with winAPI functions
"""
from synchronization import Synchronization
from Data_To_File import Data_to_file
import win32process
from win32event import WaitForSingleObject as Join, INFINITE
import logging

FILE_NAME = "Threads_Check.bin"
SIZE = 1000


def check_write_function(sync):
    logging.debug('begins check writing')
    for number in range(150):
        assert sync.set_value(number, number)


def check_read_function(sync):
    logging.debug('begins check writing')
    for number in range(150):
        assert (number == sync.get_value(number))
        

def main():
    """
    checks the reader and the writer methods.
    running them simultaneously
    using win32process.
    return: None
    """
    logging.debug("Begins checking for process:")
    sync = Synchronization(Data_to_file())
    logging.info("checking simple writing")
    process1 = win32process.beginthreadex(None, SIZE, check_write_function, (sync,), 0)[0]
    assert Join(process1, INFINITE) == 0
    logging.info("Check successful")
    logging.debug(f"\n" + "=" * 70 + "\n")
    logging.info("checking read")
    process1 = win32process.beginthreadex(None, SIZE, check_read_function, (sync,), 0)[0]
    assert Join(process1, INFINITE) == 0
    logging.info("Check successful")
    logging.debug(f"\n" + "=" * 70 + "\n")
    logging.info("checking multi reads")
    threads = []
    for i in range(5):
        thread = win32process.beginthreadex(None, SIZE, check_read_function, (sync,), 0)[0]
        threads.append(thread)
    for i in threads:
        assert Join(i, INFINITE) == 0
    logging.info("Check successful")
    logging.debug(f"\n" + "=" * 70 + "\n")
    logging.info("checking read against writing")
    process1 = win32process.beginthreadex(None, SIZE, check_read_function, (sync,), 0)[0]
    process2 = win32process.beginthreadex(None, SIZE, check_write_function, (sync,), 0)[0]
    assert Join(process1, INFINITE) == 0
    assert Join(process2, INFINITE) == 0
    logging.info("Check successful")
    logging.debug(f"\n" + "=" * 70 + "\n")
    logging.info("checking write against reading")
    process1 = win32process.beginthreadex(None, SIZE, check_write_function, (sync,), 0)[0]
    process2 = win32process.beginthreadex(None, SIZE, check_read_function, (sync,), 0)[0]
    assert Join(process1, INFINITE) == 0
    assert Join(process2, INFINITE) == 0
    logging.info("Check successful")
    logging.debug(f"\n" + "=" * 70 + "\n")
    logging.info("checking load")
    threads = []
    for i in range(15):
        thread = win32process.beginthreadex(None, SIZE, check_read_function, (sync,), 0)[0]
        threads.append(thread)
    for i in range(5):
        process1 = win32process.beginthreadex(None, SIZE, check_write_function, (sync,), 0)[0]
        threads.append(process1)
    for i in threads:
        assert Join(i, INFINITE) == 0
    logging.info("Check successful")
    logging.debug(f"\n" + "=" * 70 + "\n")
    logging.info("checking if the values stayed the same")
    process1 = win32process.beginthreadex(None, SIZE, check_read_function, (sync,), 0)[0]
    assert Join(process1, INFINITE) == 0
    logging.info("Check successful")


if __name__ == '__main__':
    logging.basicConfig(filename="CheckThread.log", filemode="a", level=logging.DEBUG)
    main()
