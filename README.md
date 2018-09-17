# webmin-alpine
[![](https://images.microbadger.com/badges/version/livinphp/webmin-alpine.svg)](https://microbadger.com/images/livinphp/webmin-alpine "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/livinphp/webmin-alpine.svg)](https://microbadger.com/images/livinphp/webmin-alpine "Get your own image badge on microbadger.com")

Docker alpine + webmin + bind9 + nginx, Provide Extensive DNS for local area networks

## Webmin Default Login (https://localhost:10000)
* __USER__: root
* __PASSWORD__: root

## SSH Default Login
* __USER__: root
* __PASSWORD__: root

## Usage
```bash
# for test, for pro remove --rm
docker run -d --rm --name webmin -h webmin \
  -p 10000:10000 -p 2020:22 \
  -p 53:53/udp -p 53:53/tcp \
  -p 80:80 \
  livinphp/webmin-alpine
# ssh test, default shell zsh,  
ssh -p 2020 root:root@localhost
# or
docker exec -it webmin /bin/zsh
```

## Packages included
* S6 overlay v1.21.2.2
* webmin v1.890
* bind latest
* nginx latest
* openssl perl perl-net-ssleay apkbuild-cpan expect git openssh rsync pwgen netcat-openbsd bash zsh
* oh-my-zsh

## Exposed ports
* 22
* 53/tcp 53/udp
* 80
* 443
* 953
* 10000

## Exposed volumes
* /etc/webmin
* /var/webmin
* /etc/bind
* /var/cache/bind
* /etc/nginx
* /var/www/html

