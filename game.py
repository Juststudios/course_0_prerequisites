play = True

array = [[".", ".", "."],
         [".", ".", "."],
         [".", ".", "."]]

game = True
isXTurn = True


# def play(isXTurn, array):
#     if isXTurn:
#         X = int(input("CHOOSE YOUR X AXIS"))
#         Y = int(input("CHOOSE YOUR Y AXIS"))
#         if array[X][Y] == "":
#             array[X][Y] = "X"
#             isXTurn = False
#     else :
#         X = int(input("CHOOSE YOUR X AXIS"))
#         Y = int(input("CHOOSE YOUR Y AXIS"))
#         if array[X][Y] == "":
#             array[X][Y] = "O"
#             isXTurn = True
#     return isXTurn
#     return array

def winCheck(gam):
    if array[0][0] == array[0][1] == array[0][2] == "X":
        print("X has won")
        gam = False
    if array[1][0] == array[1][1] == array[1][2] == "X":
        print("X has won")
        gam = False
    if array[2][0] == array[2][1] == array[2][2] == "X":
        print("X has won")
        gam = False
    if array[0][0] == array[1][0] == array[2][0] == "X":
        print("X has won")
        gam = False
    if array[0][1] == array[1][1] == array[2][1] == "X":
        print("X has won")
        gam = False
    if array[0][2] == array[1][2] == array[2][2] == "X":
        print("X has won")
        gam = False
    if array[0][0] == array[1][1] == array[2][2] == "X":
        print("X has won")
        gam = False
    if array[2][0] == array[1][1] == array[0][2] == "X":
        print("X has won")
        gam = False
    if array[0][0] == array[0][1] == array[0][2] == "O":
        print("0 has won")
        gam = False
    if array[1][0] == array[1][1] == array[1][2] == "O":
        print("0 has won")
        gam = False
    if array[2][0] == array[2][1] == array[2][2] == "O":
        print("0 has won")
        gam = False
    if array[0][0] == array[1][0] == array[2][0] == "O":
        print("0 has won")
        gam = False
    if array[0][1] == array[1][1] == array[2][1] == "O":
        print("0 has won")
        gam = False
    if array[0][2] == array[1][2] == array[2][2] == "O":
        print("0 has won")
        gam = False
    if array[0][0] == array[1][1] == array[2][2] == "O":
        print("0 has won")
        gam = False
    if array[2][0] == array[1][1] == array[0][2] == "O":
        print("0 has won")
        gam = False

    return gam


def viewGame(array):
    for x in range(3):
        print(array[x][0] + "     " + array[x][1] + "     " + array[x][2] + "\n")


viewGame(array)
while play:
    print("")
    array = [[".", ".", "."],
             [".", ".", "."],
             [".", ".", "."]]
    while game:
        try:
            if isXTurn:
                print("It is X turn")
                Y = int(input("CHOOSE YOUR X AXIS"))
                X = int(input("CHOOSE YOUR Y AXIS"))
                if array[X][Y] == ".":
                    array[X][Y] = "X"
                    isXTurn = False
                else:
                    print("Invalid position")


            else:
                print("It is O turn")
                Y = int(input("CHOOSE YOUR X AXIS"))
                X = int(input("CHOOSE YOUR Y AXIS"))
                if array[X][Y] == ".":
                    array[X][Y] = "O"
                    isXTurn = True
                else:
                    print("Invalid position")
        except ValueError:
            print("Invalid character")
        except IndexError:
            print("Invalid Position")
        game = winCheck(game)
        viewGame(array)

    next = int(input("what would you like to Do \n 1.Play again \n 2. Quit"))
    invalid = True
    while invalid:
        if next == 1:
            game = True
            invalid = False
        elif next == 2:
            play = False
            invalid = False
        else:
            print("Enter a valid input")
