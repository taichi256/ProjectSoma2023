class BitBoard():
        
    def __init__(self,board_size,board0=None,board1=None,turn=0):
        self.board_size=board_size
        self.board=[board0,board1]
        self.turn=turn
        if board0==None:
            self.board[0]=0x0000000810000000
        if  board1==None:
            self.board[1]=0x0000001008000000
        
        
    def make_mask(self,x,y):
        mask= 0x8000000000000000
        if type(x)==int:
            mask=mask>>x
        else:
            mask=mask>>("abcdefgh".index(x))
        return mask>>((int(y)-1)*8)
    
    def transfer(self,put,k):
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
    
    def makeLegalBoard(self):
        horizontalBoard=self.board[1-self.turn] & 0x7e7e7e7e7e7e7e7e
        verticalBoard=self.board[1-self.turn] & 0x00FFFFFFFFFFFF00
        allSideBoard=self.board[1-self.turn] & 0x00FFFFFFFFFFFF00
        blankBoard= 0xFFFFFFFFFFFFFFFF ^ (0x0000000000000000 | self.board[0] | self.board[1])
        legalBoard=0
        #左右
        for f in lambda x:x << 1,lambda x:x >> 1:
            tmp=horizontalBoard&(f(self.board[self.turn]))
            for _ in range(5):
                tmp|=horizontalBoard&(f(tmp))
            legalBoard|= blankBoard&(f(tmp))
        #上下
        for f in lambda x:x << 8,lambda x:x >> 8:
            tmp=verticalBoard&(f(self.board[self.turn]))
            for _ in range(5):
                tmp|=verticalBoard&(f(tmp))
            legalBoard|= blankBoard&(f(tmp))
        #斜め
        for f in lambda x:x << 7,lambda x:x>>7,lambda x:x>>9,lambda x:x<<9:
            tmp=allSideBoard&(f(self.board[self.turn]))
            for _ in range(5):
                tmp|=allSideBoard&(f(tmp))
            legalBoard|= blankBoard&(f(tmp))
        return legalBoard
    
    def choose_pos(self,x,y):
        pos=self.make_mask(x,y)
        rev=0
        for k in range(8):
            mask=self.transfer(pos,k)
            rev_=0
            while mask!=0 and (mask & self.board[1-self.turn])!=0:
                rev_|=mask
                mask=self.transfer(mask,k)
            if mask & self.board[self.turn] !=0:
                rev|=rev_
        lis=[0,0]
        lis[self.turn]=self.board[self.turn]^(pos|rev)
        lis[1-self.turn]=self.board[1-self.turn]^rev
        return BitBoard(self.board_size,lis[0],lis[1],(self.turn+1)%2)
    
    def count(self,i):
        return self.board[i].bit_count()
    
    def isPass(self):
        now=self.makeLegalBoard()
        self.turn=1-self.turn
        next=self.makeLegalBoard()
        self.turn=1-self.turn
        if (not now) and next:
            return True
        return False
    
    def isFinished(self):
        now=self.makeLegalBoard()
        self.turn=1-self.turn
        next=self.makeLegalBoard()
        self.turn=1-self.turn
        if (not now) and (not next):
            return True
        return False

    def visualize(self):
        tmp_zero=self.board[0]
        tmp_one=self.board[1]
        mask=0x8000000000000000
        for i in range(self.board_size):
            ans=[]
            for j in range(self.board_size):
                if tmp_zero & mask:
                    ans.append('x')
                elif tmp_one & mask:
                    ans.append('o')
                else:
                    ans.append('-')
                tmp_zero=tmp_zero<<1
                tmp_one=tmp_one<<1
            print(''.join(ans))

def changeZeroBitTable(line):
    #BitBoardの形式に入力を変換
    line=line.replace('1','.')
    line=line.replace('0','1')
    return int('0b'+line.replace('.','0'),0)

def changeOneBitTable(line):
    #BitBoardの形式に入力を変換
    return int('0b'+line.replace('.','0'),0)

def estimate(x,y,bitboard):
    #手の評価
    return 1

def solve(bitboard):
    #本編
    legalBoard=bitboard.makeLegalBoard()
    mask=0x8000000000000000
    ma=-1
    choose=-1
    for i in range(64):
        if legalBoard & mask:
            x=i%8
            y=i//8
            es=estimate(x,y,bitboard)
            if es>ma:
                ma=es
                choose=i
        legalBoard<<=1
    return 'abcdefgh'[choose%8]+str(choose//8+1)

_id = int(input())
board_size = int(input())

# game loop
while True:
    lines=''
    for i in range(board_size):
        lines+=input()  
    action_count = int(input())  
    bb=BitBoard(8,changeZeroBitTable(lines),changeOneBitTable(lines),_id)
    for i in range(action_count):
        action = input()  
    print(solve(bb))