import json
import subprocess
import os
from typing import Dict, List

def run_playbook(playbook_path: str, inventory_path: str) -> subprocess.CompletedProcess[str]:
    cmd = [
        'ansible-playbook',
        playbook_path,
        '-i', inventory_path,
        '--verbose',
    ]

    return subprocess.run(cmd, capture_output=True, text=True)

def run_check_load_playbook(
        playbook_path: str,
        inventory_path: str,
        metrics_dir_path: str,
        servers: List[str]
) -> Dict[str, Dict[str, float]]:

    result = run_playbook(playbook_path, inventory_path)

    if result.returncode != 0:
        raise RuntimeError(f"ERROR: Ошибка выполнения Ansible playbook: {result.stderr}")

    metrics: Dict[str, Dict[str, float]] = {}

    for server in servers:
        metric_file = os.path.join(metrics_dir_path, f"{server}.json")

        try:
            with open(metric_file, 'r') as f:
                server_metrics = json.load(f)
                metrics[server] = {
                    'memory': float(server_metrics['memory']),
                    'disk': float(server_metrics['disk']),
                    'cpu': float(server_metrics['cpu'])
                }
        except FileNotFoundError:
            raise FileNotFoundError(f"ERROR: Файл метрик не найден для сервера {server}")
        except json.JSONDecodeError:
            raise ValueError(f"ERROR: Некорректный JSON в файле метрик для сервера {server}")
        except KeyError as e:
            raise KeyError(f"ERROR: Отсутствует метрика {e} в файле для сервера {server}")

    return metrics