import socket

def get_container_ip(container_name):
    try:
        return socket.gethostbyname(container_name)
    except socket.gaierror as e:
        print(f"DNS resolution failed: {e}")
        return None