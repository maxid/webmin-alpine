FROM alpine:edge

MAINTAINER maxid <maxid@qq.com>
LABEL description='Webmin + Bind9 + Nginx: Provide Extensive DNS for local area networks'

# CREDITS
# https://github.com/smebberson/docker-alpine
# https://github.com/just-containers/base-alpine

ARG S6_OVERLAY_VERSION=v1.21.2.2 
ARG WEBMIN_VERSION=1.890 

COPY config/webmin.exp /

### S6 overlay
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
    apk --update upgrade && apk add curl && \
    curl -L -s https://github.com/just-containers/s6-overlay/releases/download/${S6_OVERLAY_VERSION}/s6-overlay-amd64.tar.gz \
    | tar xvzf - -C / && \
### Install packages
    apk add ca-certificates openssl perl perl-net-ssleay apkbuild-cpan expect nginx bind bash git openssh rsync pwgen netcat-openbsd zsh && \
### Configure zsh
    sed -i -e "s/bin\/ash/bin\/zsh/" /etc/passwd && \
### Generate Host ssh Keys
    mkdir -p ~root/.ssh && chmod 700 ~root/.ssh/ && \
    echo -e "Port 22\n" >> /etc/ssh/sshd_config && \
    cp -a /etc/ssh /etc/ssh.cache && \
### Update root password
### CHANGE IT # to something like root:wcLa3dTUQp
    echo "root:root" | chpasswd && \
### Enable ssh for root
    printf "\\nPermitRootLogin yes" >> /etc/ssh/sshd_config && \
### Enable this option to prevent SSH drop connections
    printf "\\nClientAliveInterval 15\\nClientAliveCountMax 8" >> /etc/ssh/sshd_config && \
### Configure nginx
    mkdir -p /var/log/nginx && \
    mkdir -p /var/www/html && \
    mkdir -p /etc/nginx/sites-available && \
    mkdir -p /etc/nginx/sites-enabled && \
### Install & Configure webmin
    mkdir -p /opt && cd /opt && \
    wget -q -O - "https://prdownloads.sourceforge.net/webadmin/webmin-${WEBMIN_VERSION}.tar.gz" | tar xz && \
    ln -sf /opt/webmin-${WEBMIN_VERSION} /opt/webmin && \
    /usr/bin/expect /webmin.exp && rm /webmin.exp && \
    wget -q https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O - | zsh || true && \
# Clean packages cache
    rm -rf /var/cache/apk/*

# init config file
COPY config/opt/webmin/nginx /opt/webmin/nginx
COPY config/etc/webmin /etc/webmin
# root filesystem (S6 config files)
COPY rootfs /

RUN chown -R root:bin /opt/webmin/nginx && chown -R root:bin /etc/webmin && \
    chown -R root:named /etc/bind && chown named:named /etc/bind/rndc.key

ENV SHELL /bin/zsh

EXPOSE 22 53/udp 53/tcp 80 443 953 10000

VOLUME ["/etc/webmin" , "/var/webmin" , "/etc/bind" , "/var/cache/bind" , "/etc/nginx" , "/var/www/html"]

# S6 init script
ENTRYPOINT [ "/init" ]