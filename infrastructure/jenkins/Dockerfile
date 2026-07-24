FROM jenkins/jenkins:lts

USER root

# --------------------------------------------------------
# Packages
# --------------------------------------------------------

RUN apt-get update && \
    apt-get install -y \
        git \
        curl \
        wget \
        unzip \
        python3 \
        python3-pip \
        python3-venv \
        ca-certificates \
        gnupg \
        lsb-release && \
    rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------
# Docker CLI
# --------------------------------------------------------

RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | \
    gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo $VERSION_CODENAME) stable" \
    > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------
# kubectl
# --------------------------------------------------------

RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    install -m 0755 kubectl /usr/local/bin/kubectl && \
    rm kubectl

# --------------------------------------------------------
# Minikube
# --------------------------------------------------------

RUN curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && \
    install minikube-linux-amd64 /usr/local/bin/minikube && \
    rm minikube-linux-amd64

# --------------------------------------------------------
# Jenkins Plugins
# --------------------------------------------------------

COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

RUN jenkins-plugin-cli \
    --plugin-file /usr/share/jenkins/ref/plugins.txt

USER jenkins