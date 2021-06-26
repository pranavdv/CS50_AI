from minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 4
WIDTH = 4
MINES = 4

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

revealed = set()
flags = set()
lost = False

while not lost:
    
    for i in range(HEIGHT):
        print("--" * 2*WIDTH + "-")
        for j in range(WIDTH):
            if game.is_mine((i,j)) and lost:
                print('| * ',end='')
            elif (i,j) in revealed :
                neighbours = game.nearby_mines((i,j))
                print(f"| {neighbours} ",end='')
            else : print("|   ",end='')
        print("|")
    print("--" *2* WIDTH + "-")
    
    i,j = map(int,input().split())

    move = None

    if (i,j) == (-1,-1) and not lost :
        move = ai.make_safe_move()
        if move is None:
            move = ai.make_random_move()
            if move is None:
                flags = ai.mines.copy()
                print("No moves left to make.")
            else:
                print("No known safe moves, AI making random move.")
        else:
            print("AI making safe move.")
    
    elif not lost :
        move = (i,j)

    if move is not None :
        print(move)
        if game.is_mine(move):
            lost = True
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)