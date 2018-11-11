from unittest import TestCase
from time import time
import os

from dir_dict import DirDict


class TestBase(TestCase):

    def test__create_from_non_existing(self):
        non_existing_dir = './tmp' + str(time())
        dir_dict = DirDict(non_existing_dir)
        self.assertEqual(os.path.exists(non_existing_dir), True)
        os.rmdir(non_existing_dir)

class TestFunctional(TestCase):

    def setUp(self):
        self.path = './tmp' + str(time())
        self.dictionary = DirDict(self.path)

    def tearDown(self):
        for filename in os.listdir(self.path):
            os.remove(os.path.join(self.path, filename))
        os.rmdir(self.path)

    def test__empty_dir(self):
        filename = "not_exist.txt"
        self.assertEqual(len(self.dictionary), 0)
        with self.assertRaises(IndexError):
            self.dictionary[filename]
        with self.assertRaises(SyntaxError):
            self.dictionary[''] = 'test'
        with self.assertRaises(SyntaxError):
            self.dictionary['']
    
    def test__get_and_set(self):
        filename1 = "first.txt"
        text1 = "first"
        text2 = "second"
        self.assertEqual(self.dictionary.__setitem__(filename1, text1), None)
        self.assertEqual(self.dictionary[filename1], text1)
        self.assertEqual(len(self.dictionary), 1)
        self.assertEqual(self.dictionary.__setitem__(filename1, text2), None)
        self.assertEqual(self.dictionary[filename1], text2)
        self.assertEqual(len(self.dictionary), 1)

    def test__delete(self):
        filename1 = "first.txt"
        filename2 = "second.txt"
        text1 = "one"
        text2 = "two"

        self.assertEqual(self.dictionary.__setitem__(filename1, text1), None)
        self.assertEqual(self.dictionary.__setitem__(filename2, text2), None)
        
        self.assertEqual(len(self.dictionary), 2)
        self.assertEqual(self.dictionary.__delitem__(filename1), None)
        self.assertEqual(len(self.dictionary), 1)
        with self.assertRaises(IndexError):
            self.dictionary[filename1]
        self.assertEqual(self.dictionary.__delitem__(filename2), None)
        self.assertEqual(len(self.dictionary), 0)

    def test__loop(self):
        filenames = ["first.txt", "second.txt", "third.txt"]
        texts = ["one", "two", "three"]
        
        
        for i in range(3):
            with self.subTest(i=i):
                self.assertEqual(self.dictionary.__setitem__(filenames[i], texts[i]), None)
        
        self.assertEqual(len(self.dictionary), 3)
        
        iterator = self.dictionary.__iter__()
        for i in range(3):
            with self.subTest(i=i):
                self.assertEqual(self.dictionary[iterator.__next__()], texts[i])
        
        iterator = self.dictionary.items()
        for i in range(3):
            with self.subTest(i=i):
                self.assertEqual(iterator.__next__()[1], texts[i])


class SomeInformation:

    def __str__(self):
        return "Hello, my name is Michael!"

class TestAdvanced(TestCase):

    def setUp(self):
        self.path = './tmp' + str(time())
        self.dictionary = DirDict(self.path)

    def tearDown(self):
        for filename in os.listdir(self.path):
            os.remove(os.path.join(self.path, filename))
        os.rmdir(self.path)

    def test__list_info(self):
        filename = "first.txt"
        info = [1,2,3,4,5]

        self.assertEqual(self.dictionary.__setitem__(filename, info), None)
        self.assertEqual(self.dictionary[filename], str(info))

    def test__class_info(self):
        filename = "first.txt"
        info = SomeInformation()

        self.assertEqual(self.dictionary.__setitem__(filename, info), None)
        self.assertEqual(self.dictionary[filename], str(info))

    def test__no_cached(self):
        filename = "first.txt"
        info = "some info"

        self.assertEqual(self.dictionary.__setitem__(filename, info), None)
        self.assertEqual(self.dictionary[filename], info)

        with open(os.path.join(self.path, filename), 'w') as f:
            new_info = "new info"
            f.write(new_info)
            info = new_info

        self.assertEqual(self.dictionary[filename], info)

