import socket
from concurrent.futures import ThreadPoolExecutor

def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            return port, True
        else:
            return port, False

def scan_ports(host, start_port, end_port, num_threads=100):
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(check_port, host, port) for port in range(start_port, end_port + 1)]
        
        for future in futures:
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
    
    return open_ports

def main():
    print("Добро пожаловать в сканер портов!")
    
    host = input("Введите хост (например, 127.0.0.1 или example.com): ")
    start_port = int(input("Введите начальный порт: "))
    end_port = int(input("Введите конечный порт: "))
    
    print(f"Сканирование портов от {start_port} до {end_port} на хосте {host}...")
    open_ports = scan_ports(host, start_port, end_port)
    
    if open_ports:
        print(f"Открытые порты: {', '.join(map(str, open_ports))}")
    else:
        print("Открытых портов не найдено.")

if __name__ == "__main__":
    main()
