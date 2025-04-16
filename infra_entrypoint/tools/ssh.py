import socket
import time
import subprocess

def wait_for_ssh(host, port, timeout=300):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=2):
                return True
        except (ConnectionRefusedError, socket.timeout):
            time.sleep(1)
    return False

def ssh_via_cli(private_key_path, user, host, port):
    try:
        result = subprocess.run([
            'ssh',
            '-i', private_key_path,
            '-o', 'StrictHostKeyChecking=no', # Доверяем при первом подключении к серверу
            '-o', 'ConnectTimeout=5',
            f'{user}@{host}', '-p', str(port),
            'echo connected'
        ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True, text=True)

        return result.stdout.strip() == 'connected'
    except subprocess.CalledProcessError:
        return False