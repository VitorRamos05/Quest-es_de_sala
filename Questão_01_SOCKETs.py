import socket, sys

# --------------------------------------------------
PORT        = 80
CODE_PAGE   = 'utf-8'
BUFFER_SIZE = 256
# --------------------------------------------------

host = input('\nInforme o nome do HOST ou URL do site: ')

try:
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.settimeout(None)
    requisicao = f'GET / HTTP/1.1\r\nHost: {host}\r\nAccept: text/html\r\n\r\n'
    tcp_socket.connect((host, PORT))
    tcp_socket.sendall(requisicao.encode(CODE_PAGE))

    total_length = 0
    
    while True:
        try:
            resposta = tcp_socket.recv(BUFFER_SIZE).decode(CODE_PAGE)
            total_length += len(resposta)
            if not resposta or len(resposta) < BUFFER_SIZE:
                break
            print(resposta)
        
        except KeyboardInterrupt:
            print('\nInterrupção do teclado detectada.')
            print(f'Total de bytes recebidos: {total_length}')
            tcp_socket.close()
            sys.exit()

    print(f'Total de bytes recebidos: {total_length}')
    tcp_socket.close()

except socket.error as e:
    print(f'Erro: {e}')

except Exception as e:
    print(f'Erro inesperado: {e}')
