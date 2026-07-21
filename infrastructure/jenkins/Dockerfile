FROM jenkins/jenkins:lts

USER root

# ==========================================
# System packages
# ==========================================

RUN apt-get update && \
    apt-get install -y \
        git \
        curl \
        python3 \
        python3-pip \
        python3-venv \
        ca-certificates \
        gnupg \
        lsb-release && \
    rm -rf /var/lib/apt/lists/*

# ==========================================
# Install Docker CLI
# ==========================================

RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | \
    gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo ${VERSION_CODENAME}) stable" \
    > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*

# ==========================================
# Give Jenkins access to Docker socket
# ==========================================

ARG DOCKER_GID=984

RUN if ! getent group ${DOCKER_GID}; then \
        groupadd -g ${DOCKER_GID} docker-host; \
    fi && \
    usermod -aG ${DOCKER_GID} jenkins

# ==========================================
# Jenkins Plugins
# ==========================================

COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

RUN jenkins-plugin-cli \
    --plugin-file /usr/share/jenkins/ref/plugins.txt

# ==========================================
# Switch back to Jenkins user
# ==========================================

USER jenkins