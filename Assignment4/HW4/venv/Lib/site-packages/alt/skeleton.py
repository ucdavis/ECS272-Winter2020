import shutil
import os


def get_skeleton(dst=None):
    if dst is None:
        dst = os.path.join(os.getcwd(), 'skeleton')
    src = os.path.join(os.path.dirname(__file__), 'skeleton')
    try:
        shutil.copytree(src, dst)
        print('See functional skeleton at {}'.format(dst))
        print('Test it by copy/paste/execute the below command')
        print('python {}/testRunner.py'.format(dst))
    except FileExistsError:
        print('Destination {} exists. Please remove this directory or specify a new location'.format(dst))