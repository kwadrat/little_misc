#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Remove columns and rows of pixels:
- transparent
- of uniform color
'''

import sys
import unittest
import argparse

from PIL import Image


def is_still_visible(im_x):
    return 0 not in im_x.size


def make_smaller(im_y, dst_size):
    return im_y.crop(dst_size)


def get_uni_color(im_k, col_b_x, h_ls):
    first_pixel = im_k.getpixel((col_b_x, 0))
    for y in h_ls[1:]:
        if im_k.getpixel((col_b_x, y)) != first_pixel:
            first_pixel = None
            break
    return first_pixel


def horizontal_to_vertical(im_n, jump_type):
    return im_n.transpose(jump_type)


class VanishGatherer:
    def __init__(self):
        '''
        VanishGatherer:
        '''
        self.result = '1'
        self.my_ls = []

    def remove_it(self, one_a_index):
        '''
        VanishGatherer:
        '''
        self.my_ls.append(one_a_index)

    def coherent_segment(self, one_b_index):
        '''
        VanishGatherer:
        '''
        self.last_elem = one_b_index

    def any_data(self):
        '''
        VanishGatherer:
        '''
        return self.first_elem is not None

    def start_place(self, bbb):
        '''
        VanishGatherer:
        '''
        self.first_elem = bbb
        self.coherent_segment(bbb)

    def initial_empty(self):
        '''
        VanishGatherer:
        '''
        self.start_place(None)

    def range_detected(self):
        '''
        VanishGatherer:
        '''
        return self.first_elem != self.last_elem

    def jump_too_large(self):
        '''
        VanishGatherer:
        '''
        if self.range_detected():
            self.out_ls.append('%d-%d' % (self.first_elem, self.last_elem))
        else:
            self.out_ls.append('%d' % self.first_elem)

    def get_removed(self):
        '''
        VanishGatherer:
        '''
        self.my_ls.sort()
        self.out_ls = []
        self.initial_empty()
        for one_elem in self.my_ls:
            if self.first_elem is None:
                self.start_place(one_elem)
            elif one_elem == self.last_elem + 1:
                self.coherent_segment(one_elem)
            else:
                self.jump_too_large()
                self.start_place(one_elem)
        if self.any_data():
            self.jump_too_large()
        return ', '.join(self.out_ls)


class GreenBarn:
    def __init__(self):
        '''
        GreenBarn:
        '''

    def has_some_data(self, im_g, col_x, h_ls):
        '''
        GreenBarn:
        Detect columns that are not totally transparent.
        '''
        data_detected = 0
        first_pixel = im_g.getpixel((col_x, 0))
        if first_pixel[3] == 0:
            for y in h_ls[1:]:
                if im_g.getpixel((col_x, y)) != first_pixel:
                    data_detected = 1
                    break
        else:
            data_detected = 1
        return data_detected

    def copy_pixel_column(self, im_f, dst_x, src_x, h_ls):
        '''
        GreenBarn:
        '''
        if dst_x < src_x:
            for y in h_ls:
                im_f.putpixel((dst_x, y), im_f.getpixel((src_x, y)))

    def eliminate_blanks(self, im_e):
        '''
        GreenBarn:
        '''
        if not is_still_visible(im_e):
            print('Skipping blanks')
            return im_e
        before_a_shape = im_e.size
        w, h = before_a_shape
        h_ls = list(range(h))
        dst_a_place = 0
        vanish_a_gatherer = VanishGatherer()
        for x in range(w):
            if self.has_some_data(im_e, x, h_ls):
                self.copy_pixel_column(im_e, dst_a_place, x, h_ls)
                dst_a_place += 1
            else:
                vanish_a_gatherer.remove_it(x)
        dst_a_size = 0, 0, dst_a_place, h
        if self.verbose:
            print('Removed blanks: %s %s %s' % (
                vanish_a_gatherer.get_removed(),
                before_a_shape,
                dst_a_size[-2:],
                ))
        return make_smaller(im_e, dst_a_size)

    def eliminate_redundants(self, im_j):
        '''
        GreenBarn:
        '''
        if not is_still_visible(im_j):
            print('Skipping redundants')
            return im_j
        vanish_b_gatherer = VanishGatherer()
        before_b_shape = im_j.size
        w, h = before_b_shape
        h_ls = list(range(h))
        dst_b_place = 0
        prev_color = None
        for x in range(w):
            cur_color = get_uni_color(im_j, x, h_ls)
            one_decision = None not in (prev_color, cur_color) and prev_color == cur_color
            if one_decision:
                vanish_b_gatherer.remove_it(x)
            else:
                self.copy_pixel_column(im_j, dst_b_place, x, h_ls)
                dst_b_place += 1
            prev_color = cur_color
        dst_b_size = 0, 0, dst_b_place, h
        if self.verbose:
            print('Removed redundants: %s %s %s' % (
                vanish_b_gatherer.get_removed(),
                before_b_shape,
                dst_b_size[-2:],
                ))
        return make_smaller(im_j, dst_b_size)

    def read_image_file(self, gfx_file_name):
        '''
        GreenBarn:
        '''
        return Image.open(gfx_file_name)

    def data_acquire(self, gfx_file_name):
        '''
        GreenBarn:
        '''
        self.gfx_file_name = gfx_file_name
        im_a = self.read_image_file(self.gfx_file_name)
        if self.verbose:
            self.shape_before = im_a.size
        return im_a

    def save_result(self, im_m):
        '''
        GreenBarn:
        '''
        error_occured = 1
        if is_still_visible(im_m):
            out_name = 'gen_' + self.gfx_file_name
            im_m.save(out_name)
            print("Saved as '%s'" % out_name)
            error_occured = 0
        else:
            print('Image was reduced too much after removing columns, no saving.')
        return error_occured

    def show_info_on_screen(self, im_l):
        '''
        GreenBarn:
        '''
        if self.verbose:
            print("Final reduction: %s -> %s" % (
                self.shape_before,
                im_l.size,
                ))

    def fn_processing(self, gfx_file_name):
        '''
        GreenBarn:
        '''
        im_z = self.data_acquire(gfx_file_name)
        if not self.skip_col:
            im_y = self.eliminate_blanks(im_z)
            im_z = self.eliminate_redundants(im_y)
        if not self.skip_row:
            im_w = horizontal_to_vertical(im_z, Image.ROTATE_90)
            im_v = self.eliminate_blanks(im_w)
            im_u = self.eliminate_redundants(im_v)
            im_z = horizontal_to_vertical(im_u, Image.ROTATE_270)
        self.show_info_on_screen(im_z)
        return self.save_result(im_z)

    def fn_main(self, gfx_file_name, skip_col, skip_row, verbose):
        '''
        GreenBarn:
        '''
        self.skip_col = skip_col
        self.skip_row = skip_row
        self.verbose = verbose
        return self.fn_processing(gfx_file_name)


class TestGaps(unittest.TestCase):
    def test_gaps_simple(self):
        '''
        TestGaps:
        '''
        obj = VanishGatherer()
        obj.remove_it(1)
        self.assertEqual(obj.get_removed(), '1')
        obj.remove_it(3)
        self.assertEqual(obj.get_removed(), '1, 3')
        obj.remove_it(5)
        self.assertEqual(obj.get_removed(), '1, 3, 5')

    def test_gaps_with_ranges(self):
        '''
        TestGaps:
        '''
        obj = VanishGatherer()
        self.assertEqual(obj.get_removed(), '')
        obj.remove_it(0)
        self.assertEqual(obj.get_removed(), '0')
        obj.remove_it(2)
        self.assertEqual(obj.get_removed(), '0, 2')
        obj.remove_it(3)
        self.assertEqual(obj.get_removed(), '0, 2-3')
        obj.remove_it(5)
        self.assertEqual(obj.get_removed(), '0, 2-3, 5')


def recognize_rd_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--src_file',
        default=None,
        help='Source image filename',
        )
    parser.add_argument(
        '--skip_col',
        action='store_true', default=False,
        help='Columns will stay untouched',
        )
    parser.add_argument(
        '--skip_row',
        action='store_true', default=False,
        help='Rows will stay untouched',
        )
    parser.add_argument(
        '--run_tests',
        action='store_true', default=False,
        help='Run unit tests',
        )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true', default=False,
        help='Verbose output',
        )
    return parser, parser.parse_args()


def do_my_main():
    error_occured = 1
    parser, opt_bag = recognize_rd_options()
    gfx_file_name = opt_bag.src_file
    if opt_bag.run_tests:
        unittest.main(argv=sys.argv[:1])
    green_barn = GreenBarn()
    if gfx_file_name is not None:
        error_occured = green_barn.fn_main(
            gfx_file_name,
            opt_bag.skip_col,
            opt_bag.skip_row,
            opt_bag.verbose,
        )
    else:
        parser.print_help()
    return error_occured


if __name__ == '__main__':
    error_occured = do_my_main()
    sys.exit(error_occured)
