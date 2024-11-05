import socket

def check_kafka_broker(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)  # Timeout for the connection attempt (in seconds)
        try:
            s.connect((host, port))
            print("Connection successful. The broker is reachable.")
        except socket.timeout:
            print("Connection timed out. The broker may be unreachable or down.")
        except socket.error as e:
            print(f"Connection failed: {e}")

# Test the Kafka broker connection
check_kafka_broker("85.209.163.202", 19092)
