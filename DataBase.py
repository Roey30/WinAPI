"""
Name : Roey Firan
Program name : Data_Base WinAPI
Date : 24/12/2022
Description: Data to file class - takes the database and transfer it into the file
"""
import logging
from pickle import loads, dumps
import win32file
from DataBase import *

FILE_NAME = "data_to_file.bin"


class Data_to_file(Database):
    """
    Data to file class
    """

    def __init__(self):
        """

        """
        super().__init__()

    def set_value(self, key, val):
        """
        set value function
        :param key: int
        :param val: int
        :return: result, int
        """
        try:
            self.load_pickle()
            result = super().set_value(key, val)
            self.dump_pickle()
            return result
        except OSError as err:
            logging.error(f"Data to File: Got Error {err} for the file {FILE_NAME}, returning False for failure")
            return False

    def get_value(self, key):
        """
        get value function.
        :param key: int
        :return: val, int
        """
        self.load_pickle()
        return super().get_value(key)

    def delete_value(self, key):
        """
        deletes the value of the given key
        :param key: int
        :return: val, int
        """
        self.load_pickle()
        result = super().delete_value(key)
        self.dump_pickle()
        return result

    def load_pickle(self):
        """
        reads database from the saved file
        """
        file = win32file.CreateFileW(FILE_NAME, win32file.GENERIC_READ, win32file.FILE_SHARE_READ,
                                     None, win32file.OPEN_ALWAYS, 0, None)
        logging.debug(f"Data to File: opens file to read {FILE_NAME}")
        try:
            info = win32file.ReadFile(file, 100000000)
            assert info[0] == 0
            self.dictionary = loads(info[1])
        except EOFError:
            self.dictionary = {}
        finally:
            win32file.CloseHandle(file)
            logging.debug(f"Data to File: load data to file {FILE_NAME}")

    def dump_pickle(self):
        """
        writes the database to the file 
        """
        logging.debug(f"Data to File: opens the file for write {FILE_NAME}")
        file = win32file.CreateFileW(FILE_NAME, win32file.GENERIC_WRITE, 0, None, win32file.CREATE_ALWAYS, 0, None)
        try:
            win32file.WriteFile(file, dumps(self.dictionary))
            logging.debug(f"Data to file: dumps the data to the file {FILE_NAME}")
        finally:
            win32file.CloseHandle(file)


if __name__ == '__main__':
    logging.basicConfig(filename="Data_To_File.log", filemode="a", level=logging.DEBUG)
