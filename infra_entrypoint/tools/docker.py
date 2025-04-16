import subprocess
import shutil


def check_docker_daemon():
    try:
        subprocess.run(['docker', 'info'], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        print("ERROR: Docker не установлен или не добавлен в PATH.")
        return False

def run_docker_compose(context):
    if not shutil.which("docker-compose") and not shutil.which("docker"):
        print("ERROR: Утилита docker-compose не найдена. Убедитесь, что она установлена.")
        return False

    try:
        subprocess.run(
            ['docker-compose', 'up', '-d'],
            cwd=context,
            check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print("INFO: Сеть Docker успешно запущена.")
        return True
    except subprocess.CalledProcessError as e:
        print("ERROR: Не удалось запустить сеть Docker", e)
        return False