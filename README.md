# webmin-alpine
alpine + webmin + bind9 + nginx

# Run test
```bash
docker run -d --rm --name webmin -h webmin \
  -p 10000:10000 -p 2020:22 \
  livinphp/webmin-alpine
```

