from infra_entrypoint.infra_entrypoint import infra_entrypoint
from infra_entrypoint.tools import docker

if __name__ == '__main__':
    infra_entrypoint('../infrastructure/')
    print("INFO: pg-deployer запущен. Его выполнение может занять несколько минут. Не прерывайте программу.")
    docker.execute_command_in_container("ansible_control_node",
                                        "python3 /pg-deployer/pg_deployer.py debian_ssh almalinux_ssh")