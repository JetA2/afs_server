# Wait for network connection before starting server
until ping -c1 -W1 192.168.10.10 > /dev/null; do sleep 0; done;
/usr/bin/python /root/afs/afs_server/afs_server.py &
