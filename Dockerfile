FROM python:3.7.5

RUN set -ex && \
    dpkg --add-architecture i386 & \
    apt-get update & \
    apt-get -y install gnupg2 software-properties-common & \
    wget -qO - https://dl.winehq.org/wine-builds/winehq.key | sudo apt-key add - & \
    apt-add-repository https://dl.winehq.org/wine-builds/debian/ & \
    wget -O- -q https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10/Release.key | sudo apt-key add - & \
    echo "deb http://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10 ./" | sudo tee /etc/apt/sources.list.d/wine-obs.list & \


EXPOSE 8000

CMD ["bash"]