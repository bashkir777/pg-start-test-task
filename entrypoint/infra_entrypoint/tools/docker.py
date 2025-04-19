import subprocess
import shutil


def check_docker_daemon() -> bool:
    try:
        subprocess.run(['docker', 'info'], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        print("ERROR: Docker не установлен или не добавлен в PATH.")
        return False

def run_docker_compose(context: str) -> bool:
    if not shutil.which("docker-compose") and not shutil.which("docker"):
        print("ERROR: Утилита docker-compose не найдена. Убедитесь, что она установлена.")
        return False
    try:
        subprocess.run(
            ['docker-compose', 'up', '--build','-d'],
            cwd=context,
            check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print("INFO: Сеть Docker успешно запущена.")
        return True
    except subprocess.CalledProcessError as e:
        print("ERROR: Не удалось запустить сеть Docker", e)
        return False

def execute_command_in_container(container_name: str, command: str) -> str | None:
    try:
        result = subprocess.run(
            ['docker', 'exec', container_name, 'bash', '-c', command],
            # stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Команда завершилась с ошибкой: {e.stderr}")
        return None
    except FileNotFoundError:
        print("ERROR: Docker не установлен или не добавлен в PATH.")
        return None
    except Exception as e:
        print(f"ERROR: Неизвестная ошибка: {str(e)}")
        return None