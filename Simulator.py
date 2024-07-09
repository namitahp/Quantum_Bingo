import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator



def create_board():
    board = []
    entered_numbers = set()
    print("Enter 9 unique numbers for your 3x3 Bingo board (numbers between 1 and 9 only):")
    for i in range(3):
        row = []
        for j in range(3):
            while True:
                try:
                    number = int(input(f"Enter number for position ({i+1}, {j+1}): "))
                    if number < 1 or number > 9:
                        print("Number must be between 1 and 9.")
                    elif number in entered_numbers:
                        print("Number already entered. Please enter a unique number.")
                    else:
                        row.append(number)
                        entered_numbers.add(number)
                        break
                except ValueError:
                    print("Invalid input. Please enter a number.")
        board.append(row)
    return board

def print_board(board):
    for row in board:
        print(" | ".join(str(num) if isinstance(num, int) else num for num in row))
    print("\n")

def check_bingo(board):
    for i in range(3):
        if all(num == 'X' for num in board[i]) or all(board[j][i] == 'X' for j in range(3)):
            return True
    if all(board[i][i] == 'X' for i in range(3)) or all(board[i][2-i] == 'X' for i in range(3)):
        return True
    return False

def strike_number(number, player_striked):
    for i in range(3):
        for j in range(3):
            if isinstance(player1_board[i][j], int) and player1_board[i][j] == number:
                player1_board[i][j] = 'X'
    
    for i in range(3):
        for j in range(3):
            if isinstance(player2_board[i][j], int) and player2_board[i][j] == number:
                player2_board[i][j] = 'X'

    player_striked.add(number)

def mark_superposition(num1, num2):
    for i in range(3):
        for j in range(3):
            if player1_board[i][j] == num1:
                player1_board[i][j] = f"{num1}*"
            elif player1_board[i][j] == num2:
                player1_board[i][j] = f"{num2}*"

    for i in range(3):
        for j in range(3):
            if player2_board[i][j] == num1:
                player2_board[i][j] = f"{num1}*"
            elif player2_board[i][j] == num2:
                player2_board[i][j] = f"{num2}*"

def collapse_superposition(superpositions, striked_numbers):
    backend = AerSimulator()
    for (num1, num2) in superpositions:
        circuit = QuantumCircuit(1, 1)
        circuit.h(0)
        circuit.measure(0, 0)
        job = backend.run(circuit, shots=1)
        result = job.result()
        counts = result.get_counts(circuit)
        measured_state = int(list(counts.keys())[0])
        number = num1 if measured_state == 0 else num2

        if number in striked_numbers:
            continue

        print(f"Collapsed superposition and struck off: {number}")

        original_number = num1 if number == num2 else num2
        for i in range(3):
            for j in range(3):
                if player1_board[i][j] == f"{original_number}*":
                    player1_board[i][j] = original_number
                if player1_board[i][j] == f"{number}*":
                    player1_board[i][j] = number

        for i in range(3):
            for j in range(3):
                if player2_board[i][j] == f"{original_number}*":
                    player2_board[i][j] = original_number
                if player2_board[i][j] == f"{number}*":
                    player2_board[i][j] = number

        strike_number(number, striked_numbers)

def board_filled_with_superpositions(board):
    for row in board:
        for cell in row:
            if isinstance(cell, int):
                return False
    return True

def play_bingo():
    global player1_board
    global player2_board 
    global player_striked
    print("Player 1, set up your board:")
    player1_board = create_board()
    print("Player 2, set up your board:")
    player2_board = create_board()

    player_striked = set()
    player_superpositions = []

    print("\nCurrent Boards:")
    print("Player 1's Board:")
    print_board(player1_board)
    print("\nPlayer 2's Board:")
    print_board(player2_board)
    count=0

    while True:
        if(count%2==0):
            print("\nPlayer 1's turn.")
        else:
            print("\nPlayer 2's turn.")
        mode = input("Choose mode: 1 for Classical, 2 for Quantum, 3 for Collapse: ")
        count = count + 1
        if mode == '1':  # Classical mode
            while(True):
                number = int(input("Enter a number to strike off: "))
                if(number not in range(1, 10)):
                    print("Enter a valid number")
                elif(number in player_striked):
                    print("Number already striked")
                else:
                    success = strike_number(number, player_striked)
                    break

        elif mode == '2':  # Quantum mode
            while(True):
                num1 = int(input("Enter first number for superposition: "))
                num2 = int(input("Enter second number for superposition: "))
                if(num1 < 1 or num1 > 9 or num2 < 1 or num2 > 9):
                    print("Invalid inputs. Enter again")
                elif(num1 == num2):
                    print("Enter different numbers")
                elif(num1 in player_striked or num2 in player_striked):
                    print("Number already striked")
                else:
                    mark_superposition(num1, num2)
                    player_superpositions.append((num1, num2))
                    break

        elif mode == '3':  # Collapse mode
            collapse_superposition(player_superpositions, player_striked)
            player_superpositions = []
        
        else:
            print("Invalid number entered")

        # Automatically collapse if the board is filled with superpositions
        if board_filled_with_superpositions(player1_board) or board_filled_with_superpositions(player2_board):
            print("Board is filled with superpositions. Automatically collapsing...")
            collapse_superposition(player_superpositions, player_striked)
            player_superpositions = []

        print("\nCurrent Boards:")
        print("Player 1's Board:")
        print_board(player1_board)
        print("\nPlayer 2's Board:")
        print_board(player2_board)

        if check_bingo(player1_board) and check_bingo(player2_board):
            print("It's a draw!")
            break

        if check_bingo(player1_board):
            print("Player 1 wins!")
            break
        if check_bingo(player2_board):
            print("Player 2 wins!")
            break

if __name__ == "__main__":
    play_bingo()