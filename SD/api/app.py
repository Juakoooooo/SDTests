#from flask import Flask, request, jsonify
#import redis
#import grpc
#import dns_resolver_pb2
#import dns_resolver_pb2_grpc
#import logging
#
## Configuración del registro (logging)
#logging.basicConfig(level=logging.DEBUG)
#
#app = Flask(__name__)
#
## Conexión a Redis
#try:
#    cache = redis.StrictRedis(
#        host='my-redis',  # Asegúrate de que 'my-redis' es el nombre correcto del servicio
#        port=6379,
#        decode_responses=True,
#        socket_timeout=5,  # Tiempo de espera para operaciones de socket
#        socket_connect_timeout=5  # Tiempo de espera para conectar al servidor
#    )
#    cache.ping()  # Probar conexión a Redis
#    logging.info("Conexión a Redis establecida correctamente")
#except redis.ConnectionError as e:
#    logging.error(f"Error conectando a Redis: {e}")
#    exit(1)
#except Exception as e:
#    logging.error(f"Error inesperado: {e}")
#    exit(1)
#    
#@app.route('/resolve', methods=['GET'])
#def resolve_domain():
#    domain = request.args.get('domain')
#    logging.debug(f"Received request to resolve domain: {domain}")
#    
#    if not domain:
#        logging.error("No domain provided")
#        return jsonify({"error": "No domain provided"}), 400
#
#    if cache.exists(domain):
#        ip_address = cache.get(domain)
#        logging.debug(f"Domain {domain} found in cache with IP {ip_address}")
#        return jsonify({"domain": domain, "ip": ip_address, "source": "cache"}), 200
#    
#    logging.debug(f"Domain {domain} not found in cache. Querying gRPC server.")
#    try:
#        with grpc.insecure_channel('grpc-dns-server:50051') as channel:
#            stub = dns_resolver_pb2_grpc.DNSResolverStub(channel)
#            response = stub.Resolve(dns_resolver_pb2.DNSRequest(domain=domain))
#            ip_address = response.ip
#            logging.debug(f"gRPC server returned IP {ip_address} for domain {domain}")
#            if(ip_address == ""):
#                return jsonify({"error": f"Domain {domain} not found"}), 404
#                
#            cache.set(domain, ip_address)
#            return jsonify({"domain": domain, "ip": ip_address, "source": "gRPC"}), 200
#    except grpc.RpcError as e:
#        logging.error(f"gRPC call failed: {e}")
#        return jsonify({"error": f"gRPC call failed: {e}"}), 500
#
#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
import redis
import grpc
import dns_resolver_pb2
import dns_resolver_pb2_grpc
import logging

# Configuración del registro (logging)
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Conexión a Redis
cache = None
try:
    cache = redis.StrictRedis(
        host='my-redis',
        port=6379,
        decode_responses=True,
        socket_timeout=60,  # Aumentar el tiempo de espera para operaciones de socket
        socket_connect_timeout=60  # Aumentar el tiempo de espera para conectar al servidor
    )
    cache.ping()  # Probar conexión a Redis
    logging.info("Conexión a Redis establecida correctamente")
except redis.ConnectionError as e:
    logging.error(f"Error conectando a Redis: {e}")
    # Evitar que el contenedor se cierre inmediatamente, pero loguear el error
    cache = None
except Exception as e:
    logging.error(f"Error inesperado: {e}")
    cache = None  # Asegurarse de que Redis está en None si falla la conexión inicial

@app.route('/resolve', methods=['GET'])
def resolve_domain():
    domain = request.args.get('domain')
    logging.debug(f"Received request to resolve domain: {domain}")
    
    if not domain:
        logging.error("No domain provided")
        return jsonify({"error": "No domain provided"}), 400

    # Revisar si existe en cache
    if cache and cache.exists(domain):
        ip_address = cache.get(domain)
        logging.debug(f"Domain {domain} found in cache with IP {ip_address}")
        return jsonify({"domain": domain, "ip": ip_address, "source": "cache"}), 200
    
    logging.debug(f"Domain {domain} not found in cache. Querying gRPC server.")
    try:
        # Conexión con gRPC para resolver el dominio
        with grpc.insecure_channel('grpc-dns-server:50051') as channel:
            stub = dns_resolver_pb2_grpc.DNSResolverStub(channel)
            response = stub.Resolve(dns_resolver_pb2.DNSRequest(domain=domain))
            ip_address = response.ip
            logging.debug(f"gRPC server returned IP {ip_address} for domain {domain}")
            
            # Si no se encuentra la IP, devolver 404
            if ip_address == "":
                return jsonify({"error": f"Domain {domain} not found"}), 404

            # Guardar la consulta en la cache de Redis
            if cache:
                cache.set(domain, ip_address)
                logging.debug(f"Cached {domain} with IP {ip_address}")

            return jsonify({"domain": domain, "ip": ip_address, "source": "gRPC"}), 200
    except grpc.RpcError as e:
        logging.error(f"gRPC call failed: {e}")
        return jsonify({"error": f"gRPC call failed: {e}"}), 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logging.error(f"Error al iniciar el servidor Flask: {e}")
