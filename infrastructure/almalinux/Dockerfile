FROM almalinux:8

# Установим OpenSSH сервер, Python и нужные утилиты
RUN dnf install -y \
        openssh-server \
        passwd \
        python3 \
        python3-pip \
        procps-ng \
        iproute && \
    ssh-keygen -A

# Создаем SSH-директорию для root
RUN mkdir -p /root/.ssh && \
    chmod 700 /root/.ssh && \
    chown -R root:root /root/.ssh

# Копируем публичный ключ
COPY ./ssh_keys/id_rsa.pub /root/.ssh/authorized_keys

# Устанавливаем правильные права
RUN chmod 600 /root/.ssh/authorized_keys && \
    chown root:root /root/.ssh/authorized_keys

# Разрешаем вход по ключу и отключаем пароль
RUN echo 'PubkeyAuthentication yes' >> /etc/ssh/sshd_config && \
    echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config && \
    echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config

# Открываем порт SSH
EXPOSE 22

# Запускаем SSH-демон
CMD ["/usr/sbin/sshd", "-D"]
