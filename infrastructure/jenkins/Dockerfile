FROM jenkins/jenkins:lts

USER root

# --------------------------------------------------------
# Base packages
# --------------------------------------------------------

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
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
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/debian \
$(. /etc/os-release && echo $VERSION_CODENAME) stable" \
> /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------
# kubectl
# --------------------------------------------------------

RUN curl -fsSLo /usr/local/bin/kubectl \
https://dl.k8s.io/release/$(curl -fsSL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl && \
chmod +x /usr/local/bin/kubectl

# --------------------------------------------------------
# Minikube
# --------------------------------------------------------

RUN curl -fsSLo /usr/local/bin/minikube \
https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && \
chmod +x /usr/local/bin/minikube

# --------------------------------------------------------
# Jenkins Plugins
# --------------------------------------------------------

COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

RUN jenkins-plugin-cli \
    --plugin-file /usr/share/jenkins/ref/plugins.txt

# --------------------------------------------------------
# Jenkins user
# --------------------------------------------------------

USER jenkins

WORKDIR /var/jenkins_home

ENV HOME=/var/jenkins_home