#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Symbolic equations for "Cassini Identity" in Fibonacci numbers
F(n-1) * F(n+1) - F(n)^2 == (-1) ** n
'''

import sys
import unittest


class MulClass(object):
    def __init__(self, arg_a, arg_b):
        '''
        MulClass:
        '''
        self.mlt_ls = [
            arg_a,
            arg_b,
            ]

    def get_shape(self):
        '''
        MulClass:
        '''
        return '*'.join(map(lambda x: x.get_shape(), self.mlt_ls))


class SumClass(object):
    def __init__(self):
        '''
        SumClass:
        '''
        self.sum_ls = []

    def add_to_sum(self, new_item):
        '''
        SumClass:
        '''
        self.sum_ls.append(new_item)

    def get_shape(self):
        '''
        SumClass:
        '''
        result = '+'.join(map(lambda x: x.get_shape(), self.sum_ls))
        return result


class FxRelative(object):
    def __init__(self, relative):
        '''
        FxRelative:
        '''
        self.relative = relative

    def multiply_by(self, other_one):
        '''
        FxRelative:
        '''
        return MulClass(self, other_one)

    def split_once(self):
        '''
        FxRelative:
        '''
        my_x = SumClass()
        my_x.add_to_sum(FxRelative(self.relative - 2))
        my_x.add_to_sum(FxRelative(self.relative - 1))
        return my_x

    def split_until(self, bottom_a, top_b, verbose=0):
        '''
        FxRelative:
        '''
        off_ls = [self.relative]
        while 1:
            if min(off_ls) >= bottom_a and max(off_ls) <= top_b:
                break  # Final state reached - inside expected range
            another_ls = []
            for act in off_ls:
                if bottom_a <= act <= top_b:
                    another_ls.append(act)
                else:
                    a, b = act - 2, act - 1
                    if a >= bottom_a:
                        another_ls.extend([a, b])
                    else:
                        raise RuntimeError('Za mala wartosc: %d < %d' % (a, bottom_a))
            off_ls = another_ls
        my_x = SumClass()
        off_ls.sort()
        ca = off_ls.count(bottom_a)
        cb = off_ls.count(top_b)
        if verbose:
            print('ca=%d cb=%d' % (ca, cb))
        for one_offs in off_ls:
            my_x.add_to_sum(FxRelative(one_offs))
        return my_x

    def get_shape(self):
        '''
        FxRelative:
        '''
        if self.relative:
            result = 'F(n%+d)' % self.relative
        else:
            result = 'F(n)'
        return result


class FxAbsolute(object):
    def __init__(self, absolute):
        '''
        FxAbsolute:
        '''
        self.absolute = absolute

    def split_once(self):
        '''
        FxAbsolute:
        '''
        my_x = SumClass()
        my_x.add_to_sum(FxAbsolute(self.absolute - 2))
        my_x.add_to_sum(FxAbsolute(self.absolute - 1))
        return my_x

    def get_shape(self):
        '''
        FxAbsolute:
        '''
        return 'F(%d)' % self.absolute


class TestTrials(unittest.TestCase):
    def test_1_trial(self):
        '''
        TestTrials:
        '''
        obj = FxAbsolute(0)
        self.assertEqual(obj.get_shape(), 'F(0)')

    def test_2_trial(self):
        '''
        TestTrials:
        '''
        obj = FxAbsolute(1)
        self.assertEqual(obj.get_shape(), 'F(1)')

    def test_3_trial(self):
        '''
        TestTrials:
        '''
        obj_a = FxRelative(-1)
        self.assertEqual(obj_a.get_shape(), 'F(n-1)')
        obj_b = FxRelative(1)
        self.assertEqual(obj_b.get_shape(), 'F(n+1)')
        obj_c = obj_a.multiply_by(obj_b)
        self.assertEqual(obj_c.get_shape(), 'F(n-1)*F(n+1)')

    def test_4_trial(self):
        '''
        TestTrials:
        '''
        obj_a = FxRelative(1)
        self.assertEqual(obj_a.get_shape(), 'F(n+1)')
        obj_b = obj_a.split_once()
        self.assertEqual(obj_b.get_shape(), 'F(n-1)+F(n)')

    def test_5_trial(self):
        '''
        TestTrials:
        '''
        obj_a = FxRelative(0)
        self.assertEqual(obj_a.get_shape(), 'F(n)')
        obj_b = obj_a.split_once()
        self.assertEqual(obj_b.get_shape(), 'F(n-2)+F(n-1)')

    def test_6_trial(self):
        '''
        TestTrials:
        '''
        obj_a = FxRelative(0)
        self.assertEqual(obj_a.get_shape(), 'F(n)')
        obj_b = FxRelative(2)
        self.assertEqual(obj_b.get_shape(), 'F(n+2)')
        obj_c = obj_a.multiply_by(obj_b)
        self.assertEqual(obj_c.get_shape(), 'F(n)*F(n+2)')

    def test_7_trial(self):
        '''
        TestTrials:
        '''
        obj_a = FxAbsolute(10)
        self.assertEqual(obj_a.get_shape(), 'F(10)')
        obj_b = obj_a.split_once()
        self.assertEqual(obj_b.get_shape(), 'F(8)+F(9)')

    def test_8_trial(self):
        '''
        TestTrials:
        '''
        obj_a = FxRelative(0)
        self.assertEqual(obj_a.get_shape(), 'F(n)')
        obj_b = obj_a.split_until(-3, -2)
        self.assertEqual(obj_b.get_shape(), 'F(n-3)+F(n-2)+F(n-2)')

    def test_9_trial(self):
        '''
        TestTrials:
        '''
        obj_a = FxRelative(1)
        self.assertEqual(obj_a.get_shape(), 'F(n+1)')
        obj_b = obj_a.split_until(-3, -2)
        self.assertEqual(obj_b.get_shape(), 'F(n-3)+F(n-3)+F(n-2)+F(n-2)+F(n-2)')

    def test_10_trial(self):
        '''
        TestTrials:
        '''
        obj_a = FxRelative(0)
        obj_b = obj_a.split_until(-4, -3)
        self.assertEqual(obj_b.get_shape(), 'F(n-4)+F(n-4)+F(n-3)+F(n-3)+F(n-3)')

    def test_11_trial(self):
        '''
        TestTrials:
        '''
        obj_a = FxRelative(-1)
        self.assertEqual(obj_a.get_shape(), 'F(n-1)')
        obj_b = obj_a.split_until(-3, -2)
        self.assertEqual(obj_b.get_shape(), 'F(n-3)+F(n-2)')

    def test_12_trial(self):
        '''
        TestTrials:
        '''
        obj_a = FxRelative(0)
        self.assertEqual(obj_a.get_shape(), 'F(n)')
        obj_b = obj_a.split_until(-3, -2)
        self.assertEqual(obj_b.get_shape(), 'F(n-3)+F(n-2)+F(n-2)')

    def test_13_trial(self):
        '''
        TestTrials:
        '''
        obj_a = FxRelative(1)
        obj_b = obj_a.split_until(-3, -2)
        self.assertEqual(obj_b.get_shape(), 'F(n-3)+F(n-3)+F(n-2)+F(n-2)+F(n-2)')


def do_main():
    obj_a = FxRelative(0)
    for i in range(7):
        print(i, end=' ')
        obj_b = obj_a.split_until(-i - 1, -i, verbose=1)
        print(obj_b.get_shape())


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1])
    else:
        do_main()
