#!/usr/bin/env python3

import socket
import sys
import threading
import time
import random
import os

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
bufferSize = 1024


def servirPorSiempre(socketTcp, listaconexiones):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Conectado a", client_addr)
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr])
            thread_read.start()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)


def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("hilos activos:", threading.active_count())
    print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    print(listaconexiones)


def recibir_datos(conn, addr):
    try:
        count = 0
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
        while True:
            data = conn.recv(bufferSize)
            dificultad = int.from_bytes(data, "big")
            print("Recibido,", dificultad, "   de ", addr)
            if dificultad == 1:
                tablero = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
                while True:
                    if horizontal(tablero, 3) == 0 and vertical(tablero, 3) == 0 and diagonal(tablero, 3) == 0:
                        conn.sendall(bytes([0]), addr)
                    if horizontal(tablero, 3) == 1 or vertical(tablero, 3) == 1 or diagonal(tablero, 3) == 1:
                        conn.sendall(bytes([1]), addr)
                        break
                    if horizontal(tablero, 3) == 2 or vertical(tablero, 3) == 2 or diagonal(tablero, 3) == 2:
                        conn.sendall(bytes([2]), addr)
                        break
                    data = conn.recv(bufferSize)
                    x = int.from_bytes(data, "big")
                    data = conn.recv(bufferSize)
                    y = int.from_bytes(data, "big")
                    tablero[x][y] = 'X'
                    print(tablero)
                    # determinar ganador
                    if horizontal(tablero, 3) == 0 and vertical(tablero, 3) == 0 and diagonal(tablero, 3) == 0:
                        conn.sendall(bytes([0]))
                    if horizontal(tablero, 3) == 1 or vertical(tablero, 3) == 1 or diagonal(tablero, 3) == 1:
                        conn.sendall(bytes([1]))
                        break
                    if horizontal(tablero, 3) == 2 or vertical(tablero, 3) == 2 or diagonal(tablero, 3) == 2:
                        conn.sendall(bytes([2]))
                        break
                    count += 1
                    if count == 9:
                        break
                    else:
                        while True:
                            x_server = random.randint(0, 2)
                            y_server = random.randint(0, 2)
                            if tablero[x_server][y_server] == '-':
                                conn.sendall(bytes([x_server]))
                                conn.sendall(bytes([y_server]))
                                break
                            else:
                                print("Ocupado :c")
                        count += 1
                        print("Tiro Servidor")
                        tablero[x_server][y_server] = 'O'
                        print(tablero)
            if dificultad == 2:
                tablero = [['-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-'],
                           ['-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-']]
                while True:
                    if horizontal(tablero, 5) == 0 and vertical(tablero, 5) == 0 and diagonal(tablero, 5) == 0:
                        conn.sendall(bytes([0]))
                    if horizontal(tablero, 5) == 1 or vertical(tablero, 5) == 1 or diagonal(tablero, 5) == 1:
                        conn.sendall(bytes([1]))
                        break
                    if horizontal(tablero, 5) == 2 or vertical(tablero, 5) == 2 or diagonal(tablero, 5) == 2:
                        conn.sendall(bytes([2]))
                        break
                    data = conn.recv(bufferSize)
                    x = int.from_bytes(data, "big")
                    data = conn.recv(bufferSize)
                    y = int.from_bytes(data, "big")
                    tablero[x][y] = 'X'
                    print(tablero)
                    # determinar ganador
                    if horizontal(tablero, 5) == 0 and vertical(tablero, 5) == 0 and diagonal(tablero, 5) == 0:
                        conn.sendall(bytes([0]))
                    if horizontal(tablero, 5) == 1 or vertical(tablero, 5) == 1 or diagonal(tablero, 5) == 1:
                        conn.sendall(bytes([1]))
                        break
                    if horizontal(tablero, 5) == 2 or vertical(tablero, 5) == 2 or diagonal(tablero, 5) == 2:
                        conn.sendall(bytes([2]))
                        break
                    count += 1
                    if count == 25:
                        break
                    else:
                        while True:
                            x_server = random.randint(0, 4)
                            y_server = random.randint(0, 4)
                            if tablero[x_server][y_server] == '-':
                                conn.sendall(bytes([x_server]))
                                conn.sendall(bytes([y_server]))
                                break
                            else:
                                print('Ocupado')
                        count += 1
                        print("Tiro Servidor")
                        tablero[x_server][y_server] = 'O'
                        print(tablero)
            break
    except Exception as e:
        print(e)
    finally:
        conn.close()


def horizontal(tablero, n):
    server_win = 0
    client_win = 0
    for i in range(n):
        for j in range(n):
            if tablero[i][j] == 'O':
                server_win += 1
            if tablero[i][j] == 'X':
                client_win += 1
        if n == 3 and client_win == 3:
            return 1
        if n == 3 and server_win == 3:
            return 2
        if n == 5 and client_win == 5:
            return 1
        if n == 5 and server_win == 5:
            return 2
        server_win = 0
        client_win = 0
    return 0


def vertical(tablero, n):
    server_win = 0
    client_win = 0
    for j in range(n):
        for i in range(n):
            if tablero[i][j] == 'O':
                server_win += 1
            if tablero[i][j] == 'X':
                client_win += 1
        if n == 3 and client_win == 3:
            return 1
        if n == 3 and server_win == 3:
            return 2
        if n == 5 and client_win == 5:
            return 1
        if n == 5 and server_win == 5:
            return 2
        server_win = 0
        client_win = 0
    return 0


def diagonal(tablero, n):
    server_win = 0
    client_win = 0
    for i in range(n):
        for j in range(n):
            if tablero[i][j] == 'O' and i == j:
                server_win += 1
            if tablero[i][j] == 'X' and i == j:
                client_win += 1
    if n == 3 and client_win == 3:
        return 1
    if n == 3 and server_win == 3:
        return 2
    if n == 5 and client_win == 5:
        return 1
    if n == 5 and server_win == 5:
        return 2
    server_win = 0
    client_win = 0
    for i in range(n):
        for j in range(n):
            if tablero[i][j] == 'O' and (i + j) == (n - 1):
                server_win += 1
            if tablero[i][j] == 'X' and (i + j) == (n - 1):
                client_win += 1
    if n == 3 and client_win == 3:
        return 1
    if n == 3 and server_win == 3:
        return 2
    if n == 5 and client_win == 5:
        return 1
    if n == 5 and server_win == 5:
        return 2
    return 0


listaConexiones = []
host, port, numConn = sys.argv[1:4]

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

serveraddr = (host, int(port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")

    servirPorSiempre(TCPServerSocket, listaConexiones)
