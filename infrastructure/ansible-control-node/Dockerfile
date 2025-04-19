FROM debian:bullseye

# Установим необходимые пакеты, включая Ansible
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        openssh-client \
        curl \
        gnupg \
        lsb-release && \
    pip3 install --no-cache-dir ansible

# Создаем SSH-директорию для root
RUN mkdir -p /root/.ssh && \
    chmod 700 /root/.ssh && \
    chown -R root:root /root/.ssh

# Копируем готовую пару ключей (закрытый и публичный)
COPY ./ssh_keys/id_rsa /root/.ssh/id_rsa
COPY ./ssh_keys/id_rsa.pub /root/.ssh/id_rsa.pub

# Устанавливаем правильные права для ключей
RUN chmod 600 /root/.ssh/id_rsa && \
    chmod 644 /root/.ssh/id_rsa.pub && \
    chown root:root /root/.ssh/id_rsa /root/.ssh/id_rsa.pub

# Запускаем bash при старте контейнера
CMD ["/bin/bash"]
