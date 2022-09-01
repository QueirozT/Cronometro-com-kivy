FROM ubuntu

# Configurações locais
RUN apt update -qq > /dev/null \
    && apt-get install -y locales \
    && locale-gen en_US.UTF-8

ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

RUN apt-get update -qq > /dev/null \
    && apt-get install -y git \
    zlib1g-dev \
    openjdk-11-jdk \
    autoconf \
    curl \
    libtool \
    libtinfo5 \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libltdl-dev \
    libncurses5-dev \
    libncursesw5-dev \
    ccache \
    unzip \
    zip \
    python3.10 \
    python3-pip \
    python3-virtualenv \
    python3-setuptools \
    pkg-config \
    cmake \
    automake \
    build-essential \
    gettext \
    patch \
    adb \
    scrcpy \
    sudo

ENV USER="user"

ENV HOME_DIR="/home/${USER}"

ENV WORK_DIR="${HOME_DIR}/buildozer" \
    SRC_DIR="${HOME_DIR}/src" \
    PATH="${HOME_DIR}/.local/bin:${PATH}"


# Preparando um ambiente sem root
RUN useradd --create-home --shell /bin/bash ${USER}

# Dando acesso ao sudo sem senha
RUN usermod -append --groups sudo ${USER}

RUN echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER ${USER}

VOLUME ${WORK_DIR}

WORKDIR ${WORK_DIR}

COPY --chown=user:user . ${SRC_DIR}

RUN python3 -m pip install --upgrade pip cython buildozer virtualenv --user

CMD buildozer android debug


### GUIA DE USO ###

## Esta imagem docker irá compilar o projeto e gerar um apk para android.
## Para usar, precisa ter um buildozer.spec e executar os comandos abaixo:


## Para buildar sua própria imagem docker:
# docker build -t <seu nome>/kivy-buildozer .

## Caso não tenha o buildozer.spec:
# docker run -it -v $PWD:/home/user/buildozer/ queirozt/kivy-buildozer buildozer init .

## Para compilar o seu app, precisa ter o buildoser.spec no diretório atual:
# docker run -it -v $PWD:/home/user/buildozer/ --name build queirozt/kivy-buildozer

## Para compilar e rodar no scrcpy (ou outro emulador):
# docker run -it --privileged --name build \
#     -v $HOME/.Xauthority:/root/.Xauthority \
#     -v $PWD:/home/user/buildozer/ \
#     -v /dev/bus/usb:/dev/bus/usb \
#     -v /tmp/.X11-unix:/tmp/.X11-unix \
#     --net=host -e DISPLAY=$DISPLAY \
#     queirozt/kivy-buildozer \
#     buildozer android debug deploy run logcat
