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


def limpiar_tablero(tablero, n):
    for i in range(n):
        for j in range(n):
            tablero[i][j] = '-'


def actualiza_tablero(tablero, n, Client_conn):
    for i in range(n):
        for j in range(n):
            Client_conn.send(tablero[i][j].encode('utf8'))
    print('Se actualizo')


def tablero_lleno(tablero, n):
    cont = 0
    for i in range(n):
        for j in range(n):
            if tablero[i][j] != '-':
                cont += 1
    if cont == 9 and n == 3:
        return 1
    if cont == 25 and n == 5:
        return 1
    return 0


def horizontal(tablero, n, simbolo):
    server_win = 0
    client_win = 0
    for i in range(n):
        for j in range(n):
            if tablero[i][j] != simbolo and tablero[i][j] != '-':
                server_win += 1
            if tablero[i][j] == simbolo:
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


def vertical(tablero, n, simbolo):
    server_win = 0
    client_win = 0
    for j in range(n):
        for i in range(n):
            if tablero[i][j] != simbolo and tablero[i][j] != '-':
                server_win += 1
            if tablero[i][j] == simbolo:
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


def diagonal(tablero, n, simbolo):
    server_win = 0
    client_win = 0
    for i in range(n):
        for j in range(n):
            if tablero[i][j] != simbolo and i == j and tablero[i][j] != '-':
                server_win += 1
            if tablero[i][j] == simbolo and i == j:
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
            if tablero[i][j] != simbolo and (i + j) == (n - 1) and tablero[i][j] != '-':
                server_win += 1
            if tablero[i][j] == simbolo and (i + j) == (n - 1):
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


def recibir_datos(Client_conn, addr):
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
        while True:
            data = Client_conn.recv(bufferSize)
            dificultad = int.from_bytes(data, "big")
            print("Recibido,", dificultad, "   de ", addr)
            if dificultad == 1:
                # print ('Ingresa el simbolo que utilizaras')
                data = Client_conn.recv(bufferSize)
                simbolo = data.decode("utf-8")
                while True:
                    actualiza_tablero(tablero3, 3, Client_conn)
                    time.sleep(2.1)
                    actualiza_tablero(tablero3, 3, Client_conn)
                    data = Client_conn.recv(bufferSize)
                    x = int.from_bytes(data, "big")
                    data = Client_conn.recv(bufferSize)
                    y = int.from_bytes(data, "big")
                    tablero3[x][y] = simbolo
                    actualiza_tablero(tablero3, 3, Client_conn)
                    print(tablero3)
                    # determinar ganador
                    if horizontal(tablero3, 3, simbolo) == 0 and vertical(tablero3, 3, simbolo) == 0 and diagonal(
                            tablero3, 3, simbolo) == 0:
                        Client_conn.send(bytes(str(0) + '\n', 'utf8'))
                    if horizontal(tablero3, 3, simbolo) == 1 or vertical(tablero3, 3, simbolo) == 1 or diagonal(
                            tablero3, 3, simbolo) == 1:
                        Client_conn.send(bytes(str(1) + '\n', 'utf8'))
                        break
                    if horizontal(tablero3, 3, simbolo) == 2 or vertical(tablero3, 3, simbolo) == 2 or diagonal(
                            tablero3, 3, simbolo) == 2:
                        Client_conn.send(bytes(str(2) + '\n', 'utf8'))
                        break
                    if tablero_lleno(tablero3, 3) == 1:
                        break
                    print(tablero3)
            if dificultad == 2:
                # print ('Ingresa el simbolo que utilizaras')
                data = Client_conn.recv(bufferSize)
                simbolo = data.decode("utf-8")
                while True:
                    data = Client_conn.recv(bufferSize)
                    x = int.from_bytes(data, "big")
                    data = Client_conn.recv(bufferSize)
                    y = int.from_bytes(data, "big")
                    tablero5[x][y] = simbolo
                    actualiza_tablero(tablero5, 5, Client_conn)
                    print(tablero5)
                    # determinar ganador
                    if horizontal(tablero5, 5, simbolo) == 0 and vertical(tablero5, 5, simbolo) == 0 and \
                            diagonal(tablero5, 5, simbolo) == 0:
                        Client_conn.send(bytes(str(0) + '\n', 'utf8'))
                    if horizontal(tablero5, 5, simbolo) == 1 or vertical(tablero5, 5, simbolo) == 1 or \
                            diagonal(tablero5, 5, simbolo) == 1:
                        Client_conn.send(bytes(str(1) + '\n', 'utf8'))
                        break
                    if horizontal(tablero5, 5, simbolo) == 2 or vertical(tablero5, 5, simbolo) == 2 or \
                            diagonal(tablero5, 5, simbolo) == 2:
                        Client_conn.send(bytes(str(2) + '\n', 'utf8'))
                        break
                    if tablero_lleno(tablero5, 5) == 1:
                        break
                    print(tablero5)
            limpiar_tablero(tablero5, 5)
            limpiar_tablero(tablero3, 3)
            break
    except Exception as e:
        print(e)
    finally:
        Client_conn.close()


tablero3 = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
tablero5 = [['-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-']]
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
