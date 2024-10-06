#  network.py
#  afs_server
#
#  Created by Peter Lundkvist on 11/12/2023.
#
#  This is free and unencumbered software released into the public domain.
#  See the file COPYING for more details, or visit <http://unlicense.org>.

import urllib.parse

GET_INSERTED_DISK = 'GET_INSERTED_DISK'
GET_FILE_LIST = 'GET_FILE_LIST'
INSERT_DISK = 'INSERT_DISK'
EJECT_DISK = 'EJECT_DISK'


def send_response(transport, response=''):
    message = 'OK'

    if (len(response) > 0):
        message += ('\n' + response)

    _write_message(transport, message)


def send_error(transport, *error):
    message = 'ERROR'

    if (len(error) > 0):
        message += ('\n' + ' '.join(part for part in error))

    _write_message(transport, message)


def parse_request(data):
    message = urllib.parse.unquote_plus(data.decode().strip())
    request = None

    # Arguments are all text after the first space
    args = message.split(' ', 1)
    if (len(args) > 1):
        message = args[0]
        args = args[1]
    else:
        args = None

    if (message == GET_INSERTED_DISK):
        request = GET_INSERTED_DISK
    elif (message == GET_FILE_LIST):
        request = GET_FILE_LIST
    elif (message == INSERT_DISK):
        request = INSERT_DISK
    elif (message == EJECT_DISK):
        request = EJECT_DISK

    return request, args


def _write_message(transport, message):
    message = urllib.parse.quote_plus(message) + '\n'

    transport.write(message.encode())
