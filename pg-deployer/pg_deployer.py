import os
import sys

from tools import ansible

service_metrics_directory = '/tmp/server_metrics'
ansible_playbooks_directory = '/pg-deployer/ansible-playbooks'
check_load_playbook = os.path.join(ansible_playbooks_directory, 'check_load.yml')
install_postgres_playbook = os.path.join(ansible_playbooks_directory, 'install_postgres_server.yml')
install_postgres_client_playbook = os.path.join(ansible_playbooks_directory, 'install_postgres_client.yml')
configure_postgres_playbook = os.path.join(ansible_playbooks_directory, 'configure_postgres_server.yml')
inventory = os.path.join(ansible_playbooks_directory, 'inventory.ini')

if __name__ == "__main__":
    first_server = sys.argv[1]
    second_server = sys.argv[2]

    with open(inventory, 'w') as f:
        f.write("[all]\n")
        f.write(first_server + "\n")
        f.write(second_server + "\n")

    print(f"INFO pg-deployer: Запускаем проверку загруженности серверов {first_server}, {second_server}")

    load_dict = ansible.run_check_load_playbook(check_load_playbook, inventory,
                                          service_metrics_directory, [first_server, second_server])

    filtered_load_dict = {
        k: v for k, v in load_dict.items()
        if v["memory"] >= 1000 and v["disk"] >= 2000
    }

    if len(filtered_load_dict) == 0:
        print("ERROR pg-deployer: Предоставленные сервера не соответствуют минимально необходимым требованиям по памяти для установки и запуска PostgreSQL.")
        print("Требования:")
        print("    RAM >= 1000 MB")
        print("    Disk >= 2000 MB")
        exit(1)

    min_cpu_load = min([_["cpu"] for _ in filtered_load_dict.values()])

    postgres_hostname = None
    for key, value in filtered_load_dict.items():
        if value["cpu"] == min_cpu_load:
            postgres_hostname = key

    postgres_client_hostname = second_server if postgres_hostname == first_server else first_server

    print(f"INFO pg-deployer: Наименее загруженный сервер - {postgres_hostname}")

    with open(inventory, 'w') as f:
        f.write("[all]\n")
        f.write(postgres_hostname + "\n")

    print(f"INFO pg-deployer: Запускаем установку PostgreSQL и инициализацию кластера на {postgres_hostname}")
    install_postgres_result = ansible.run_playbook(install_postgres_playbook, inventory)

    if install_postgres_result.returncode == 0:
        print("INFO pg-deployer: Установка PostgreSQL и инициализация кластера завершена успешно.")
    else:
        print("ERROR pg-deployer: Установка PostgreSQL и инициализация кластера завершились с ошибкой.")
        print(f"ERROR pg-deployer: Код возврата: {install_postgres_result.returncode}")
        print(f"ERROR pg-deployer: Стандартный вывод:\n{install_postgres_result.stdout}")
        print(f"ERROR pg-deployer: Стандартный поток ошибок:\n{install_postgres_result.stderr}")
        exit(1)

    print(f"INFO pg-deployer: Запускаем конфигурацию PostgreSQL и старт работы кластера на {postgres_hostname}")
    configure_postgres_result = ansible.run_playbook_with_extra_vars(configure_postgres_playbook, inventory,
                                                                     {'student_allowed_host': postgres_client_hostname})

    if configure_postgres_result.returncode == 0:
        print("INFO pg-deployer: Кластер PostgreSQL успешно сконфигурирован и запущен.")
    else:
        print("ERROR pg-deployer: Конфигурация и запуск кластера PostgreSQL завершилась ошибкой.")
        print(f"ERROR pg-deployer: Код возврата: {configure_postgres_result.returncode}")
        print(f"ERROR pg-deployer: Стандартный вывод:\n{configure_postgres_result.stdout}")
        print(f"ERROR pg-deployer: Стандартный поток ошибок:\n{configure_postgres_result.stderr}")
        exit(1)

    with open(inventory, 'w') as f:
        f.write("[all]\n")
        f.write(postgres_client_hostname + "\n")

    print(f"INFO pg-deployer: Запускаем установку клиента PostgreSQL на {postgres_client_hostname}")
    install_postgres_client_result = ansible.run_playbook(install_postgres_client_playbook, inventory)

    if install_postgres_client_result.returncode == 0:
        print(f"INFO pg-deployer: Клиент PostgreSQL успешно установлен на {postgres_client_hostname}.")
    else:
        print(f"ERROR pg-deployer: Установка клиента PostgreSQL на {postgres_client_hostname} завершилась ошибкой.")
        print(f"ERROR pg-deployer: Код возврата: {install_postgres_client_result.returncode}")
        print(f"ERROR pg-deployer: Стандартный вывод:\n{install_postgres_client_result.stdout}")
        print(f"ERROR pg-deployer: Стандартный поток ошибок:\n{install_postgres_client_result.stderr}")
        exit(1)