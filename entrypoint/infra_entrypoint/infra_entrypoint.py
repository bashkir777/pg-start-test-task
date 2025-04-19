from .tools.key_gen import generate_ssh_keypair
from .tools.docker import *
from .tools.ssh import *
import os

def infra_entrypoint(
    path_to_infrastructure: str,
    ssh_keys_subdir: str = 'ssh_keys',
    public_ssh_key_name: str = 'id_rsa.pub',
    private_ssh_key_name: str = 'id_rsa',
    debian_port: int = 2222,
    alma_linux_port: int = 2223,
    host: str = '127.0.0.1',
    ssh_timeout: int = 300
) -> None:
    ssh_keys_directory = os.path.join(path_to_infrastructure, ssh_keys_subdir)
    os.makedirs(ssh_keys_directory, exist_ok=True)

    public_ssh_key_path = os.path.join(ssh_keys_directory, public_ssh_key_name)
    private_ssh_key_path = os.path.join(ssh_keys_directory, private_ssh_key_name)

    if not os.path.exists(public_ssh_key_path) or not os.path.exists(private_ssh_key_path):
        print("INFO: Генерируем пару SSH ключей")
        generate_ssh_keypair(save_dir=ssh_keys_directory, private_key_name=private_ssh_key_name)
        print(f"INFO: Пара SSH ключей была успешно создана и сохранена в директорию: {ssh_keys_directory}")
    else:
        print("INFO: Пара SSH ключей уже существует и будет использована для запуска инфраструктуры")

    if not check_docker_daemon():
        print("ERROR: Docker демон не запущен. Пожалуйста, запустите Docker Desktop или службу Docker.")
        exit(1)

    print("INFO: Docker демон запущен.")

    print("INFO: Запускаем сеть Docker. Это может занять несколько минут.")

    if not run_docker_compose(path_to_infrastructure):
        print("ERROR: Не удалось запустить сеть Docker.")
        exit(1)

    if not wait_for_ssh(host, debian_port, ssh_timeout):
        print("ERROR: не удалось получить доступ к Debian серверу")
        exit(1)

    print(f"INFO: Debian сервер успешно запущен и прослушивает порт {debian_port}")

    if not wait_for_ssh(host, alma_linux_port, ssh_timeout):
        print("ERROR: не удалось получить доступ к AlmaLinux серверу")
        exit(1)

    print(f"INFO: AlmaLinux сервер успешно запущен и прослушивает порт {alma_linux_port}")

