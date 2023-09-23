#!/bin/bash
# comment
[ -z $(find -type f -name ".env") ] && cp .env.example .env
[ -z $(docker volume ls | awk '{print $2}' | grep -E flastrukt-api_databases) ] && docker volume create flastrukt-api_databases
[ -z $(docker network ls | awk '{print $2}' | grep -E flastrukt_net) ] && docker network create flastrukt_net
while :
do
read -r -p "Do you want to use the --build flag? [yY/nN/qQ] " input
case $input in
      [yY])
            docker-compose -f docker-compose.yml up --build
            exit 0
            ;;
      [nN])
            docker-compose -f docker-compose.yml up
            exit 0
            ;;
      [qQ])
            echo "Quitting..."
            exit 0
            ;;
             *)
            echo "Invalid input, FUCK YOU..."
            ;;
esac
done
