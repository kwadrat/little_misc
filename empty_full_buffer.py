#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Calculate free space and number of elements available in a buffer
./empty_full_buffer.py --test; red_green_bar.py $? $COLUMNS

red_green_bar.py from https://github.com/kwadrat/rgb_tdd
'''

import sys
import argparse
import unittest

class Buffer(object):
    def __init__(self):
        '''
        Buffer:
        '''

    def crossing_end(self):
        '''
        Buffer:
        '''
        return self.first_free < self.first_ready

    def free_space(self):
        '''
        Buffer:
        '''
        result = self.first_ready - self.first_free - 1
        if result < 0:
            result += self.total
        return result

    def elements_available(self):
        '''
        Buffer:
        '''
        result = self.first_free - self.first_ready
        if result < 0:
            result += self.total
        return result

    def set_params(self, total, first_free, first_ready):
        '''
        Buffer:
        '''
        self.total = total
        self.first_free = first_free
        self.first_ready = first_ready
        a = self.elements_available()
        b = self.free_space()
        c = a + b
        if c != self.total - 1:
            raise RuntimeError("Elements + Free should be Buffer Size decreased by 1: a = %d b = %d c = %d" % (a, b, c))


class TestSpaceAndElements(unittest.TestCase):
    def test_space_and_elements(self):
        '''
        TestSpaceAndElements:
        '''
        obj = Buffer()
        if 1:
            obj.set_params(total=10, first_free=0, first_ready=0)
            self.assertEqual(obj.free_space(), 9)
            self.assertEqual(obj.elements_available(), 0)
        if 1:
            obj.set_params(total=10, first_free=1, first_ready=0)
            self.assertEqual(obj.free_space(), 8)
            self.assertEqual(obj.elements_available(), 1)
        if 1:
            obj.set_params(total=10, first_free=2, first_ready=0)
            self.assertEqual(obj.free_space(), 7)
            self.assertEqual(obj.elements_available(), 2)
        if 1:
            obj.set_params(total=11, first_free=0, first_ready=0)
            self.assertEqual(obj.free_space(), 10)
            self.assertEqual(obj.elements_available(), 0)
        if 1:
            obj.set_params(total=10, first_free=2, first_ready=1)
            self.assertEqual(obj.free_space(), 8)
            self.assertEqual(obj.elements_available(), 1)
        if 1:
            obj.set_params(total=10, first_free=0, first_ready=9)
            self.assertEqual(obj.free_space(), 8)
            self.assertEqual(obj.elements_available(), 1)
        if 1:
            obj.set_params(total=10, first_free=1, first_ready=9)
            self.assertEqual(obj.free_space(), 7)
            self.assertEqual(obj.elements_available(), 2)
        if 1:
            obj.set_params(total=10, first_free=1, first_ready=8)
            self.assertEqual(obj.free_space(), 6)
            self.assertEqual(obj.elements_available(), 3)
        if 1:
            obj.set_params(total=11, first_free=1, first_ready=8)
            self.assertEqual(obj.free_space(), 6)
            self.assertEqual(obj.elements_available(), 4)
        if 1:
            obj.set_params(total=12, first_free=1, first_ready=8)
            self.assertEqual(obj.free_space(), 6)
            self.assertEqual(obj.elements_available(), 5)


def recognize_buffer_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test',
        action='store_true', default=False,
        help='Run unittests')
    opt_bag = parser.parse_args()
    return opt_bag


if __name__ == '__main__':
    current_state = 0
    opt_bag = recognize_buffer_options()
    if opt_bag.test:
        current_state = unittest.main(argv=sys.argv[:1])
    sys.exit(current_state)
