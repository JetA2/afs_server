GET_FILE_LIST = 'GET_FILE_LIST'
INSERT_DISK = 'INSERT_DISK'
EJECT_DISK = 'EJECT_DISK'


def send_response(transport, *lines):
    _write_line(transport, 'OK')

    for line in lines:
        _write_line(transport, line)


def send_error(transport, *error):
    _write_line(transport, ' '.join(part for part in error))


def parse_request(data):
    message = data.decode().strip()
    request = None

    # Arguments are all text after the first space
    args = message.split(' ', 1)
    if (len(args) > 1):
        message = args[0]
        args = args[1]
    else:
        args = None

    if (message == GET_FILE_LIST):
        request = GET_FILE_LIST
    elif (message == INSERT_DISK):
        request = INSERT_DISK
    elif (message == EJECT_DISK):
        request = EJECT_DISK

    return request, args


def _write_line(transport, line):
    message = line + '\n'

    transport.write(message.encode())
