# docker/attacker/Dockerfile
FROM alpine:latest

# Installer curl pour générer du trafic
RUN apk add --no-cache curl

# Script qui génère du trafic vers la cible
CMD while true; do curl -s http://target:3000 > /dev/null; done
