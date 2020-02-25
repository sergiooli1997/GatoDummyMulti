#!/usr/bin/env python3

import socket
import time
import random
import os

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
bufferSize = 1024


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


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
    UDPServerSocket.bind((HOST, PORT))
    print("El servidor TCP está disponible y en espera de solicitudes")
    count = 0
    while True:
        print("Esperando a recibir datos... ")
        data, address = UDPServerSocket.recvfrom(bufferSize)
        dificultad = int.from_bytes(data, "big")
        print("Recibido,", dificultad, "   de ", address)
        if dificultad == 1:
            tablero = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
            while True:
                if horizontal(tablero, 3) == 0 and vertical(tablero, 3) == 0 and diagonal(tablero, 3) == 0:
                    UDPServerSocket.sendto(bytes([0]), address)
                if horizontal(tablero, 3) == 1 or vertical(tablero, 3) == 1 or diagonal(tablero, 3) == 1:
                    UDPServerSocket.sendto(bytes([1]), address)
                    break
                if horizontal(tablero, 3) == 2 or vertical(tablero, 3) == 2 or diagonal(tablero, 3) == 2:
                    UDPServerSocket.sendto(bytes([2]), address)
                    break
                data, address = UDPServerSocket.recvfrom(bufferSize)
                x = int.from_bytes(data, "big")
                data, address = UDPServerSocket.recvfrom(bufferSize)
                y = int.from_bytes(data, "big")
                tablero[x][y] = 'X'
                print(tablero)
                # determinar ganador
                if horizontal(tablero, 3) == 0 and vertical(tablero, 3) == 0 and diagonal(tablero, 3) == 0:
                    UDPServerSocket.sendto(bytes([0]), address)
                if horizontal(tablero, 3) == 1 or vertical(tablero, 3) == 1 or diagonal(tablero, 3) == 1:
                    UDPServerSocket.sendto(bytes([1]), address)
                    break
                if horizontal(tablero, 3) == 2 or vertical(tablero, 3) == 2 or diagonal(tablero, 3) == 2:
                    UDPServerSocket.sendto(bytes([2]), address)
                    break
                count += 1
                if count == 9:
                    break
                else:
                    while True:
                        x_server = random.randint(0, 2)
                        y_server = random.randint(0, 2)
                        if tablero[x_server][y_server] == '-':
                            UDPServerSocket.sendto(bytes([x_server]), address)
                            UDPServerSocket.sendto(bytes([y_server]), address)
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
                    UDPServerSocket.sendto(bytes([0]), address)
                if horizontal(tablero, 5) == 1 or vertical(tablero, 5) == 1 or diagonal(tablero, 5) == 1:
                    UDPServerSocket.sendto(bytes([1]), address)
                    break
                if horizontal(tablero, 5) == 2 or vertical(tablero, 5) == 2 or diagonal(tablero, 5) == 2:
                    UDPServerSocket.sendto(bytes([2]), address)
                    break
                data, address = UDPServerSocket.recvfrom(bufferSize)
                x = int.from_bytes(data, "big")
                data, address = UDPServerSocket.recvfrom(bufferSize)
                y = int.from_bytes(data, "big")
                tablero[x][y] = 'X'
                print(tablero)
                # determinar ganador
                if horizontal(tablero, 5) == 0 and vertical(tablero, 5) == 0 and diagonal(tablero, 5) == 0:
                    UDPServerSocket.sendto(bytes([0]), address)
                if horizontal(tablero, 5) == 1 or vertical(tablero, 5) == 1 or diagonal(tablero, 5) == 1:
                    UDPServerSocket.sendto(bytes([1]), address)
                    break
                if horizontal(tablero, 5) == 2 or vertical(tablero, 5) == 2 or diagonal(tablero, 5) == 2:
                    UDPServerSocket.sendto(bytes([2]), address)
                    break
                count += 1
                if count == 25:
                    break
                else:
                    while True:
                        x_server = random.randint(0, 4)
                        y_server = random.randint(0, 4)
                        if tablero[x_server][y_server] == '-':
                            UDPServerSocket.sendto(bytes([x_server]), address)
                            UDPServerSocket.sendto(bytes([y_server]), address)
                            break
                        else:
                            print('Ocupado')
                    count += 1
                    print("Tiro Servidor")
                    tablero[x_server][y_server] = 'O'
                    print(tablero)
        break