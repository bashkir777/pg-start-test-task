import os
import shutil
import subprocess
import stat

def generate_ssh_keypair(save_dir: str, private_key_name: str, bits=4096) -> None:
    if not shutil.which("ssh-keygen"):
        raise RuntimeError("ERROR: ssh-keygen не найден. Установите OpenSSH или используйте альтернативный метод.")

    os.makedirs(save_dir, exist_ok=True)
    private_key_path = os.path.join(save_dir, private_key_name)
    public_key_path = private_key_path + '.pub'

    if os.path.exists(private_key_path):
        os.remove(private_key_path)
    if os.path.exists(public_key_path):
        os.remove(public_key_path)

    cmd = [
        'ssh-keygen',
        '-t', 'rsa',
        '-b', str(bits),
        '-f', private_key_path,
        '-N', ''
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"INFO: Создан приватный ssh ключ: {private_key_path}")
        print(f"INFO: Создан публичный ssh ключ: {public_key_path}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ERROR: Не удалось сгенерировать ssh ключ: {e}")

    try:
        os.chmod(public_key_path, stat.S_IRUSR | stat.S_IWUSR)
        print(f"INFO: Права на публичный ключ установлены: только для текущего пользователя (rw-------)")
        os.chmod(private_key_path, stat.S_IRUSR | stat.S_IWUSR)
        print(f"INFO: Права на приватный ключ установлены: только для текущего пользователя (rw-------)")
    except Exception as e:
        print(f"ERROR: Не удалось установить права на файл: {e}")

