"""
Name : Roey Firan
Program name : Data_Base WinAPI
Date : 24/12/2022
Description: takes care of the threading using semaphor and mutex(syncing)
"""
import logging
from win32event import CreateSemaphore, CreateMutex, ReleaseSemaphore, ReleaseMutex, WaitForSingleObject, INFINITE

NAME_READ = "read"
NAME_WRITE = "write"


class Synchronization:
    """
    Synchronize database class
    """
    def __init__(self, data_base):
        """
        Synchronize database's constructor
        :param data_base: database, object
        """
        super().__init__()
        self.dictionary = data_base
        self.write = CreateMutex(None, False, NAME_WRITE)
        self.read = CreateSemaphore(None, 10, 10, NAME_READ)

    def set_value(self, key, value):
        """
        set value function
        :param key: key in dictionary
        :param value: val in dictionary
        :return: result
        """
        WaitForSingleObject(self.write, INFINITE)
        for i in range(10):
            WaitForSingleObject(self.read, INFINITE)
        logging.debug("Sync_DataBase: self write - acquired")
        result = self.dictionary.set_value(key, value)
        ReleaseSemaphore(self.read, 10)
        ReleaseMutex(self.write)
        logging.debug("Sync_DataBase: self write - released")
        return result

    def get_value(self, key):
        """
        get value function.
        :param key: int
        :return: value, int
        """
        WaitForSingleObject(self.read, INFINITE)
        logging.debug("Sync_DataBase:  self read - acquired")
        result = self.dictionary.get_value(key)
        ReleaseSemaphore(self.read, 1)
        logging.debug("Sync_DataBase:  self read - released")
        return result

    def delete_value(self, key):
        """
        deletes the value of the given key
        :param key: int
        :return: value, int
        """
        WaitForSingleObject(self.read, INFINITE)
        logging.debug("Sync_DataBase: self write - acquired")
        self.dictionary.delete_value(key)
        ReleaseMutex(self.write)
        logging.debug("Sync_DataBase: self write - released")

    def __str__(self):
        """
        print function
        :return: str
        """
        return f'The dictionary: {self.dictionary}'


if __name__ == '__main__':
    logging.basicConfig(filename="synchronization.log", filemode="a", level=logging.DEBUG)
