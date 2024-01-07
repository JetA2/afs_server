import os.path
import errno
import random
import sh
import wave
import alsaaudio

from util import local

_USB_IMAGE_PATH = '/mnt/storage/usb_device.bin'
_FILE_LIST_PATH = '/root/afs/file_list.txt'
_INSERTED_DISK_FILE_PATH = '/root/afs/inserted.txt'
_SOUND_DIRECTORY = '/root/afs/sound'
_MSD_MODULE = 'g_mass_storage'
# _MSD_MODULE = 'crc7'  # Use for testing on systems without g_mass_storage

_ALSA_PERIOD_COUNT = 2
_ALSA_PERIOD_SIZE = 4096

_sound_device = None
_sound_insert = []
_sound_eject = []


def initialize():
    global _sound_device

    # Handle the case where the computer was reset while a disk
    # was still inserted.
    if (not _usb_device_created()):
        eject_disk()

    # Read sounds (all files must be of the same format)
    file_list = [entry for entry in os.scandir(
        _SOUND_DIRECTORY) if not entry.is_dir()]

    for entry in file_list:
        with wave.open(entry.path, 'rb') as file:
            frames = file.readframes(file.getnframes())

            if (entry.name.startswith('insert')):
                _sound_insert.append(frames)
            elif (entry.name.startswith('eject')):
                _sound_eject.append(frames)

            if (_sound_device == None):
                # Setup sound device
                format = None

                if file.getsampwidth() == 1:
                    format = alsaaudio.PCM_FORMAT_U8
                elif file.getsampwidth() == 2:
                    format = alsaaudio.PCM_FORMAT_S16_LE
                elif file.getsampwidth() == 3:
                    format = alsaaudio.PCM_FORMAT_S24_3LE
                elif file.getsampwidth() == 4:
                    format = alsaaudio.PCM_FORMAT_S32_LE
                else:
                    raise ValueError('Unsupported sound format', format)

                _sound_device = alsaaudio.PCM(channels=file.getnchannels(),
                                              rate=file.getframerate(),
                                              format=format,
                                              periods=_ALSA_PERIOD_COUNT,
                                              periodsize=_ALSA_PERIOD_SIZE)


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
    try:
        sh.grep('-q', _MSD_MODULE, _in=sh.lsmod())
        return True
    except sh.ErrorReturnCode_1:
        return False


def _create_usb_device():
    _play_sound(random.choice(_sound_insert))
    sh.modprobe(_MSD_MODULE,
                'file=' + _USB_IMAGE_PATH,
                'removable=1',
                'ro=0',
                'stall=0')


def _remove_usb_device():
    sh.modprobe('-r', _MSD_MODULE)
    _play_sound(random.choice(_sound_eject))


def _play_sound(frames):
    try:
        _sound_device.write(frames)
    except SystemError as e:
        pass  # TODO: needed until fix for https://github.com/larsimmisch/pyalsaaudio/issues/137

    _sound_device.drain()
