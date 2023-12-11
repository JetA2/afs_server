import os.path
import errno

from util import local

_USB_IMAGE_PATH = '/home/floppy_disk/usb_device.bin'
_FILE_LIST_PATH = '/home/floppy_disk/file_list.txt'
_INSERTED_DISK_FILE_PATH = '/home/floppy_disk/inserted.txt'


def initialize():
    # Handle the case where the computer was reset while a disk
    # was still inserted.
    if (not _usb_device_created()):
        eject_disk()


def get_inserted_disk():
    if (_usb_device_created()):
        with open(_INSERTED_DISK_FILE_PATH, 'r') as file:
            return file.read()

    return None


def get_cached_file_list():
    try:
        with open(_FILE_LIST_PATH, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return None


def insert_disk(name):
    # Eject any inserted disk
    eject_disk()

    # Check if the disk exists
    if (not local.disk_exists(name)):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), name)

    # Save name of disk being inserted
    with open(_INSERTED_DISK_FILE_PATH, 'w') as file:
        file.write(name)

    # Save file list
    file_list = local.get_file_list()
    file_list_string = '\n'.join(line for line in file_list)

    with open(_FILE_LIST_PATH, 'w') as file:
        file.write(file_list_string)

    # Create the init file that will determine the inserted disk
    local.create_init_file(name)

    # Unmount USB image from local file system
    local.unmount()

    # Create USB mass storage device
    _create_usb_device()


def eject_disk():
    # Remove USB mass storage device
    if (_usb_device_created()):
        _remove_usb_device()

    # Mount USB image to local filesystem
    local.mount(_USB_IMAGE_PATH)

    # Delete temporary files
    try:
        os.remove(_INSERTED_DISK_FILE_PATH)
    except FileNotFoundError:
        pass

    try:
        os.remove(_FILE_LIST_PATH)
    except FileNotFoundError:
        pass


def _usb_device_created():
    # TODO: Check if USB mass storage device is created
    return os.path.isfile(_INSERTED_DISK_FILE_PATH)


def _create_usb_device():
    pass


def _remove_usb_device():
    pass
