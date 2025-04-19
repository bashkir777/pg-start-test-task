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

    ansible.run_check_load_playbook(check_load_playbook, inventory,
                                          service_metrics_directory, [first_server, second_server])

    with open(inventory, 'w') as f:
        f.write("[all]\n")
        f.write(first_server + "\n")
        f.write(second_server + "\n")

    ansible.run_playbook(install_postgres_playbook, inventory)
