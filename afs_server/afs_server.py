import asyncio
import signal
import socket

from util import local, network, usb

SERVER_PORT = 52611
REQUEST_TIMEOUT = 3  # Seconds

shutdown_command = None


class ServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

        # Send connection response
        try:
            inserted_disk = usb.get_inserted_disk()
            network.send_response(
                self.transport, '' if inserted_disk == None else inserted_disk)
        except Exception as e:
            network.send_error(self.transport, str(e))

        # Close connection if no request is received within a time period
        loop = asyncio.get_running_loop()
        self.request_timer = loop.call_later(
            REQUEST_TIMEOUT, self.transport.close)

    def data_received(self, data):
        self.request_timer.cancel()
        self.request_timer = None

        try:
            # Handle request
            request, args = network.parse_request(data)

            if (request == network.GET_FILE_LIST):
                file_list = local.get_file_list()
                network.send_response(self.transport, *file_list)
            elif (request == network.INSERT_DISK):
                if (args != None):
                    usb.insert_disk(args)
                    network.send_response(self.transport)
                else:
                    network.send_error(
                        self.transport, 'Image path not provided')
            elif (request == network.EJECT_DISK):
                usb.eject_disk()
                network.send_response(self.transport)
            else:
                network.send_error(
                    self.transport, 'Unknown request:', data.decode())
        except Exception as e:
            network.send_error(self.transport, str(e))

        # Close the connection
        self.transport.close()

    def connection_lost(self, exception):
        if (self.request_timer != None):
            self.request_timer.cancel()


def stop():
    print('Shutting down...', flush=True)
    shutdown_command.set_result(True)


async def main():
    global shutdown_command

    # Set up signal handlers
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, stop)
    loop.add_signal_handler(signal.SIGTERM, stop)

    # Initialize to valid state
    usb.initialize()

    # Start server
    server = await loop.create_server(lambda: ServerProtocol(),
                                      host='0.0.0.0',
                                      port=SERVER_PORT)

    print('Server started!', flush=True)

    # Wait for shutdown
    shutdown_command = loop.create_future()

    try:
        await shutdown_command
    finally:
        server.close()

    print('Bye!', flush=True)

# Run main program
asyncio.run(main())
