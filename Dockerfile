FROM python:3.7.5

RUN set -ex && \
    dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get -y install gnupg2 software-properties-common && \
    wget -qO - https://dl.winehq.org/wine-builds/winehq.key | apt-key add && \
    apt-add-repository https://dl.winehq.org/wine-builds/debian && \
    wget -O- -q https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10/Release.key | apt-key add - && \
    echo "deb http://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10 ./" | tee /etc/apt/sources.list.d/wine-obs.list && \
    apt-get update && apt-get install -y --install-recommends winehq-stable


RUN set -ex && \
    apt-get install -y supervisor curl git pwgen && \
	apt-get autoclean && \
	apt-get autoremove && \
	rm -rf /var/lib/apt/lists/*

WORKDIR /alldev

EXPOSE 8000

CMD ["python3"]