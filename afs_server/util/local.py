import os
import sh

from util import usb


_MOUNT_POINT = '/mnt/usb_device'
_FF_INIT_FILE = 'FF/INIT_A.CFG'


def get_file_list():
    # Check if a cached list exists (because the image is unmounted)
    file_list = usb.get_cached_file_list()

    if (file_list == None):
        # List files from mounted image
        file_list = [file.name for file in os.scandir(_MOUNT_POINT)
                     if not file.is_dir()]
        file_list.sort()

    return file_list


def create_init_file(disk):
    path = os.path.join(_MOUNT_POINT, _FF_INIT_FILE)

    with open(path, 'w') as file:
        file.write(disk)


def disk_exists(disk):
    path = os.path.join(_MOUNT_POINT, disk)
    return os.path.isfile(path)


def mount(image):
    # Check if image is already mounted
    try:
        sh.mountpoint(_MOUNT_POINT, '-q')
    except sh.ErrorReturnCode_32:
        sh.mount(image, _MOUNT_POINT, '-o', 'users,umask=000')


def unmount():
    sh.umount(_MOUNT_POINT)
