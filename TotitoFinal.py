#Hector Miguel Valle Quinto
#17102
import socketio
import random
import numpy as np
import math
sio = socketio.Client()

#Clase Juego donde se guarda la informacion del juego actual
class Juego:
    def __init__(self):
        self.user_name = ""
        self.tournament_id = ""
        self.ready = False
        self.gameFinished = False
        self.game_id = 0
        self.oponent_id = 0
        self.player_turn_id = 0
        self.winnerTurnID = 0
        self.board = []
        self.tempboard = []
        
#Funcion en la cual se simula una de las jugadas en el tablero
#actual del juego devolviendo los puntos de la jugada
def simulateMove(playerNumber, playing, oldBoard, move):
    board = list(map(list, oldBoard))
    punteoInicial = 0
    punteoFinal = 0
    acumulador = 0
    contador = 0
    EMPTY = 99
    FILL = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2
    N = 6
    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoInicial = punteoInicial + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0
    board[move[0]][move[1]] = FILL
    acumulador = 0
    contador = 0
    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoFinal = punteoFinal + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0
    if punteoInicial < punteoFinal:
        if playerNumber == 1:
            if (punteoFinal - punteoInicial) == 2:
                board[move[0]][move[1]] = FILLEDP12
            elif (punteoFinal - punteoInicial) == 1:
                board[move[0]][move[1]] = FILLEDP11
        elif playerNumber == 2:
            if (punteoFinal - punteoInicial) == 2:
                board[move[0]][move[1]] = FILLEDP22
            elif (punteoFinal - punteoInicial) == 1:
                board[move[0]][move[1]] = FILLEDP21
    
    return (board, punteoFinal - punteoInicial) if playing else (board, (-1) * (punteoFinal - punteoInicial))

#Funcion en la cual se calcula la heuristica de la movida que se esta
#realizando sobre el tablero
def heuristic(playerNumber, playing, oldBoard, move):
    board = list(map(list, oldBoard))
    punteoInicial = 0
    punteoFinal = 0
    acumulador = 0
    contador = 0
    EMPTY = 99
    FILL = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2
    N = 6
    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoInicial = punteoInicial + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0
    board[move[0]][move[1]] = FILL
    acumulador = 0
    contador = 0
    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoFinal = punteoFinal + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0
    if punteoInicial < punteoFinal:
        if playerNumber == 1:
            if (punteoFinal - punteoInicial) == 2:
                board[move[0]][move[1]] = FILLEDP12
            elif (punteoFinal - punteoInicial) == 1:
                board[move[0]][move[1]] = FILLEDP11
        elif playerNumber == 2:
            if (punteoFinal - punteoInicial) == 2:
                board[move[0]][move[1]] = FILLEDP22
            elif (punteoFinal - punteoInicial) == 1:
                board[move[0]][move[1]] = FILLEDP21

    return punteoFinal - punteoInicial if playing else (-1) * (punteoFinal - punteoInicial)

#Funcion que devuelve una lista de movimientos posibles para que
#el jugador no haga movidas no validas
def getMoves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if int(board[i][j]) == 99:
                moves.append((i, j))

    return moves
#Funcion de minmax
def minimax(depth, playing, id, alpha, beta, board, move):
    player = id if playing else (id % 2) + 1
    if depth == 0 or 99 not in np.asarray(board).reshape(-1):
        return heuristic(player, not playing, board, move)
    board, _ = simulateMove(player, playing, board, move)
    moves = getMoves(board)
    if playing:
        maxVal = -math.inf 
        for movement in moves:
            val = minimax(depth - 1, False, player, alpha, beta, board, movement)
            maxVal = max(maxVal, val)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        board[move[0]][move[1]] = 99
        return maxVal
    else:
        minVal = math.inf
        for movement in moves:
            val = minimax(depth - 1, True, player, alpha, beta, board, movement)
            minVal = min(minVal, val)
            beta = min(beta, val)
        board[move[0]][move[1]] = 99
        return minVal
#Funcion de elegir el movivmiento en el cual se crea una lista de
#movimientos que se le pasa a minmax con el tablero que crean
#para luego sugerir un movimiento mas adecuado de acuerdo
#con lo que se encontro con el lookahead dado.
def chooseMove(id, lookahead, board):
    moves = []
    bestScore = -math.inf
    possible = getMoves(board)
    for movement in possible:
        score = minimax(int(lookahead), False, int(id), -math.inf, math.inf, board, movement)
        if score > bestScore:
            bestScore = score
            moves.clear()
        if score >= bestScore:
            moves.append(movement)
    return random.choice(moves)

@sio.on('connect')
def connect():
    # Client has connected
    print("Conectado: " + juego.user_name);
    # Signing signal
    sio.emit('signin', {
        'user_name': juego.user_name,
        'tournament_id': juego.tournament_id,  
        'user_role': "player"
    })
    
@sio.on('ready')
def on_ready(data):
    juego.gameFinished = False
    juego.game_id = data['game_id']
    juego.player_turn_id = data['player_turn_id']

    if (juego.player_turn_id == 1):
        juego.oponent_id = 2
    else:
        juego.oponent_id = 1

    #print(humanBoard(data['board']))
    
    juego.board = data['board']
    juego.tempboard = data['board']
    juego.ready = True

    movement = []

    #while probar(movement) != True:
    move = chooseMove(juego.player_turn_id, 2, juego.tempboard)
    movement = [move[0], move[1]]          
        
    print("Movement played: " + str(movement[0]) + ", " + str(movement[1]))
    sio.emit('play', {
        'tournament_id': juego.tournament_id,
        'player_turn_id': juego.player_turn_id,
        'game_id': juego.game_id,
        'movement': movement
    })
                    
@sio.on('finish')
def on_finish(data):
    juego.game_id = data['game_id']
    juego.player_turn_id = data['player_turn_id']
    juego.winner_turn_id = data['winner_turn_id']
    if data['player_turn_id'] == data['winner_turn_id']:
        print("Eres el ganador")
    else:
        print("Perdiste")
    print('Game finished!')
    juego.gameFinished = True
    sio.emit('player_ready', {
        'tournament_id': juego.tournament_id,
        'game_id': juego.game_id,
        'player_turn_id': data['player_turn_id']
    })

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")


juego = Juego()
juego.user_name = input("Ingrese su usuario: ")
juego.tournament_id = int(input("Ingrese el Tournament ID: "))
host = input("Ingrese el host: ")

sio.connect(host)
