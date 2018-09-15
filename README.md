# webmin-alpine
alpine + webmin + bind9 + nginx

# Run test
```bash
docker run -d --rm --name webmin -h webmin \
  -p 10000:10000 -p 2020:22 \
  livinphp/webmin-alpine
  
ssh -p 2020 root:root@localhost
# or
docker exec -it webmin /bin/zsh
```
> open https://localhost:10000 in browser, default user: root, pass: root

