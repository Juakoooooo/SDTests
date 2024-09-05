#!/bin/bash

# Esperar a que Redis esté en funcionamiento
until redis-cli -h my-redis -p 6379 ping | grep -q "PONG"; do
  echo "Esperando a que Redis esté listo..."
  sleep 2
done

echo "Redis está listo. Aplicando configuraciones..."

# Asignar límite de memoria y política de remoción
redis-cli -h my-redis -p 6379 CONFIG SET maxmemory 200mb
redis-cli -h my-redis -p 6379 CONFIG SET maxmemory-policy allkeys-lru

echo "Configuraciones aplicadas exitosamente."
