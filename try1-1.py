class BitBoard():
    
    def __init__(self,board_size):
        self.board_size=board_size
        self.board=[0x0000000810000000,0x0000001008000000]
        
    def __init__(self,board_size,board0,board1):
        self.board_size=board_size
        self.board=[board0,board1]
        
    def make_mask(self,x,y):
        mask= 0x8000000000000000
        mask=mask>>("abcdefgh".index(x))
        return mask>>((int(y)-1)*8)
    
    def transfer(put,k):
        if k==0:
            return (put << 8) & 0xffffffffffffff00
        elif k==1:
            return (put << 7) & 0x7f7f7f7f7f7f7f00
        elif k==2:
            return (put >> 1) & 0x7f7f7f7f7f7f7f7f
        elif k==3:
            return (put >> 9) & 0x007f7f7f7f7f7f7f
        elif k==4:
            return (put >> 8) & 0x00ffffffffffffff
        elif k==5:
            return (put >> 7) & 0x00fefefefefefefe
        elif k==6:
            return (put << 1) & 0xfefefefefefefefe
        elif k==7:
            return (put << 9) & 0xfefefefefefefe00
        
    def choose_pos(self,x,y,i):
        pos=self.make_mask(x,y)
        rev=0
        for k in range(8):
            mask=self.transfer(pos,k)
            rev_=0
            while mask!=0 and mask & self.board[1-i]:
                rev_|=mask
                mask=self.transfer(pos,k)
            if mask & self.board !=0:
                rev|=rev_
        lis=[0,0]
        lis[i]=self.board[i]^(pos|rev)
        lis[1-i]=self.board[1-i]^rev
        return BitBoard(self.board_size,lis[0],lis[1])
    
    def count(self,i):
        return self.board[i].bit_count()
'''
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def isok():
    return True

_id = int(input())  # id of your player.
board_size = int(input())

# game loop
while True:
    for i in range(board_size):
        line = input()  # rows from top to bottom (viewer perspective).
    action_count = int(input())  # number of legal actions for this turn.
    for i in range(action_count):
        action = input()  # the action

    print(action)


    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # a-h1-8
    
'''