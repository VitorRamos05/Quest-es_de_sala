import socket, sys

# --------------------------------------------------
PORT = 80
CODE_PAGE = 'utf-8'
BUFFER_SIZE = 256
# --------------------------------------------------

def parse_chunked_response(response):
    parts = response.split('\r\n', 1)
    size_hex = parts[0]
    try:
        size = int(size_hex, 16)
    except ValueError:
        return None, response

    data = parts[1][:size]
    remaining_data = parts[1][size:]
    return data, remaining_data

host = input('\nInforme o nome do HOST ou URL do site: ')

try:
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.settimeout(None)
    requisicao = f'GET / HTTP/1.1\r\nHost: {host}\r\nAccept: text/html\r\n\r\n'
    tcp_socket.connect((host, PORT))
    tcp_socket.sendall(requisicao.encode(CODE_PAGE))

    total_length = 0
    chunked_data = ''

    while True:
        try:
            resposta = tcp_socket.recv(BUFFER_SIZE).decode(CODE_PAGE)
            total_length += len(resposta)

            if 'Transfer-Encoding: chunked' in resposta:
                chunked_data += resposta
                while True:
                    chunk, remaining = parse_chunked_response(chunked_data)
                    if chunk is None:
                        break
                    print(chunk)
                    chunked_data = remaining

            else:
                print(resposta)
            if not resposta or len(resposta) < BUFFER_SIZE:
                break
        
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
