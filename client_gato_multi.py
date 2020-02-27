#!/usr/bin/env python3

import socket
import os
import time

bufferSize = 2


def imprimir_tablero(tablero, n):
    a = ""
    if n == 3:
        print('\t0' + '\t1' + '\t2')
    if n == 5:
        print('\t0' + '\t1' + '\t2' + '\t3' + '\t4')
    for i in range(n):
        print(i, end="\t")
        for j in range(n):
            a += str(tablero[i][j]) + '\t'
        print(a)
        a = ""


def actualiza_tablero(tablero, n, TCPClientSocket):
    for i in range(n):
        for j in range(n):
            data = TCPClientSocket.recv(bufferSize)
            tablero[i][j] = data.decode('utf8')


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


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    count = 0
    TCPClientSocket.connect((HOST, PORT))
    os.system("cls")
    tiempo_inicial = time.time()
    print("---------BIENVENIDO AL GATO DUMMY---------")
    print("Elige dificultad ;)")
    print("1.- Dificultad principiante")
    print("2.- Dificultad avanzada")
    dificultad = int(input())
    os.system("cls")
    TCPClientSocket.sendall(bytes([dificultad]))
    if dificultad == 1:
        tablero = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        imprimir_tablero(tablero, 3)
        print('Ingresa el simbolo que utilizaras')
        simbolo = input()
        TCPClientSocket.send(simbolo.encode('utf8'))
        while True:
            os.system("cls")
            imprimir_tablero(tablero, 3)
            while True:
                print("Elige casilla")
                x = int(input())
                y = int(input())
                if tablero[x][y] == '-':
                    TCPClientSocket.sendall(bytes([x]))
                    print('Enviado x={}'.format(x))
                    TCPClientSocket.sendall(bytes([y]))
                    print('Enviado y={}'.format(y))
                    break
                else:
                    print("Casilla Ocupada :C")
            tablero[x][y] = simbolo
            os.system("cls")
            imprimir_tablero(tablero, 3)
            actualiza_tablero(tablero, 3, TCPClientSocket)
            data = TCPClientSocket.recv(bufferSize)
            strings = data.decode('utf8')
            bandera = int(strings)
            if bandera == 0:
                pass
            else:
                print('Finalizado.')
                imprimir_tablero(tablero, 3)
                if bandera == 1:
                    print('Ganaste :D Buen juego')
                else:
                    print('Perdiste :( ')
                break
            if tablero_lleno(tablero, 3) == 1:
                break
    if dificultad == 2:
        tablero = [['-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-']]
        imprimir_tablero(tablero, 3)
        print('Ingresa el simbolo que utilizaras')
        simbolo = input()
        TCPClientSocket.send(simbolo.encode('utf8'))
        while True:
            os.system("cls")
            imprimir_tablero(tablero, 5)
            while True:
                print("Elige casilla")
                x = int(input())
                y = int(input())
                if tablero[x][y] == '-':
                    TCPClientSocket.sendall(bytes([x]))
                    print('Enviado x={}'.format(x))
                    TCPClientSocket.sendall(bytes([y]))
                    print('Enviado y={}'.format(y))
                    break
                else:
                    print("Casilla Ocupada :C")
            tablero[x][y] = simbolo
            os.system("cls")
            imprimir_tablero(tablero, 5)
            actualiza_tablero(tablero, 5, TCPClientSocket)
            data = TCPClientSocket.recv(bufferSize)
            strings = data.decode('utf8')
            bandera = int(strings)
            if bandera == 0:
                pass
            else:
                print('Finalizado.')
                imprimir_tablero(tablero, 5)
                if bandera == 1:
                    print('Ganaste :D Buen juego')
                else:
                    print('Perdiste :( ')
                break
            if tablero_lleno(tablero, 5) == 1:
                break
    tiempo_final = time.time()
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print('Duracion de la partida: %.2f segs.' % round(tiempo_ejecucion, 2))
    os.system("pause")
