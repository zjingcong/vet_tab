#!/usr/bin/env python

import os
import sys
import argparse

SCENE_PATH = 'scenes/scene_1'
SCENE_TEMPLATE = 'scenes/temp/vet_tab_test_2_temp.pbrt'
OUTPUT = '/home/jingcoz/workspace/vetTab_robustness/generator/output'


def load_temp():
    with open(SCENE_TEMPLATE, 'r') as template_file:
        template = template_file.read()

    return template


def generate(parms, template, name):
    file_name = os.path.join(SCENE_PATH, name)
    scene = template.format(**parms)
    with open(file_name, 'w') as scene_file:
        scene_file.write(scene)


if __name__ == '__main__':
    # create scene folder
    os.system("mkdir {}".format(SCENE_PATH))
    # load template
    template = load_temp()
    # create pbrt scene files
    name = SCENE_TEMPLATE.split('/')[-1].replace('temp', '{num:04}')

    ##### generate parms and fill template here, just for testing right now #####
    parms = dict(eye_x=0.0, eye_y=12.0, eye_z=8.0, trans_x=0.0, trans_y=0.0, trans_z=0.0, rot=0.0, out='../output/vet_tab_test_2.png')
    id = 0
    for eye_x in xrange(-2, 3, 2):
        for eye_y in xrange(10, 16, 2):
            for trans_x in xrange(-3, 4, 3):
                for trans_z in xrange(-3, 4, 3):
                    for rot in xrange(-10, 11, 10):
                        parms['eye_x'] = eye_x
                        parms['eye_y'] = eye_y
                        parms['trans_x'] = trans_x
                        parms['trans_z'] = trans_z
                        parms['rot'] = rot
                        parms['out'] = '{}.png'.format(os.path.join(OUTPUT, name.split('.')[-2].format(num=id)))

                        # fill template
                        generate(parms, template, name.format(num=id))
                        id = id + 1

    # final clean: chmod
    os.system("chmod 777 {}".format(SCENE_PATH))
