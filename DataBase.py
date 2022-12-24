"""
Name : Roey Firan
Program name : Data_Base WinAPI
Date : 24/12/2022
Description: DataBase class
"""


class Database:
    def __init__(self):
        self.dictionary = {}

    def set_value(self, key, val):
        self.dictionary[key] = val
        if self.dictionary[key] == val:
            return True

    def get_value(self, key):
        return self.dictionary.get(key)

    def delete_value(self, key):
        val = self.dictionary[key]
        self.dictionary.pop(key)
        return val

    def __str__(self):
        """
        print function
        :return: str
        """
        return f'The dictionary: {self.dictionary}'
