import os
import sys

from tools import ansible

service_metrics_directory = '/tmp/server_metrics'
ansible_playbooks_directory = '/pg-deployer/ansible-playbooks'
check_load_playbook = os.path.join(ansible_playbooks_directory, 'check_load.yml')
install_postgres_playbook = os.path.join(ansible_playbooks_directory, 'install_postgres.yml')
inventory = os.path.join(ansible_playbooks_directory, 'inventory.ini')

if __name__ == "__main__":
    first_server = sys.argv[1]
    second_server = sys.argv[2]

    with open(inventory, 'w') as f:
        f.write("[all]\n")
        f.write(first_server + "\n")
        f.write(second_server + "\n")

    print(f"INFO: Запускаем проверку загруженности серверов {first_server}, {second_server}")

    load_dict = ansible.run_check_load_playbook(check_load_playbook, inventory,
                                          service_metrics_directory, [first_server, second_server])

    filtered_load_dict = {
        k: v for k, v in load_dict.items()
        if v["memory"] >= 1000 and v["disk"] >= 2000
    }

    if len(filtered_load_dict) == 0:
        print("ERROR: Предоставленные сервера не соответствуют минимально необходимым требованиям по памяти для установки и запуска PostgreSQL.")
        print("Требования:")
        print("    RAM >= 1000 MB")
        print("    Disk >= 2000 MB")
        exit(1)

    min_cpu_load = min([_["cpu"] for _ in filtered_load_dict.values()])

    postgres_hostname = None
    for key, value in filtered_load_dict.items():
        if value["cpu"] == min_cpu_load:
            postgres_hostname = key

    print(f"INFO: Наименее загруженный сервер - {postgres_hostname}")

    with open(inventory, 'w') as f:
        f.write("[all]\n")
        f.write(postgres_hostname + "\n")

    print(f"INFO: Запускаем установку PostgreSQL на {postgres_hostname}")
    ansible.run_playbook(install_postgres_playbook, inventory)
