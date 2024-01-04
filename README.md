![Build Status](https://github.com/TheWicklowWolf/pyNameCheap/actions/workflows/main.yml/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/thewicklowwolf/pynamecheap.svg)

NameCheap Domain IP Updater.

## Run using docker-compose

```yaml
version: "2.1"
services:
  pynamecheap:
    image: thewicklowwolf/pynamecheap:latest
    container_name: pynamecheap
    environment:
      - domain=domainA
      - hosts=a,b,c
      - ddns_password=password
      - refresh_interval=600
    volumes:
      - /etc/localtime:/etc/localtime:ro
    restart: unless-stopped
```

---


https://hub.docker.com/r/thewicklowwolf/pynamecheap

