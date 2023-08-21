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
        allSideBoard=self.board[1-self.turn] & 0x007e7e7e7e7e7e00
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
    
    def choose_pos_int(self,x,y):
        return self.choose_pos(x,y+1)
    
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

def bitcount(n):
    #nを２進数化した時の１の数を測定
    re=0
    for i in range(64):
        re+=n&1
        n>>=1
    return re

def estimate_by_pos(bitboard):
    point=[30,-12,0,-1,-1,0,-12,30,
            -12,-15,-3,-3,-3,-3,-15,-12,
           0,-3,0,-1,-1,0,-3,0,
           -1,-3,-1,-1,-1,-1,-3,-1,
           -1,-3,-1,-1,-1,-1,-3,-1,
           0,-3,0,-1,-1,0,-3,0,
           -12,-15,-3,-3,-3,-3,-15,-12,
           30,-12,0,-1,-1,0,-12,30]
    me=bitboard.board[bitboard.turn]
    opponent=bitboard.board[1-bitboard.turn]
    re=0
    for i in range(64):
        re+=(int(me&1)-int(opponent&1))*point[63-i]
        me>>=1
        opponent>>=1
    return re

def estimate_by_way(bitboard):
    LegalBoard=bitboard.makeLegalBoard()
    bitboard.turn=1-bitboard.turn
    OpponentLegalBoard=bitboard.makeLegalBoard()
    bitboard.turn=1-bitboard.turn
    return bitcount(LegalBoard)-bitcount(OpponentLegalBoard)
    
def estimate_board(bitboard):
    return estimate_by_pos(bitboard)+estimate_by_way(bitboard)

def alphaBetaPruning(bitboard,deep,returnAction=False,alpha=None,beta=None):
    if alpha==None:
        alpha=-10**8
    if beta==None:
        beta=10**8
    if deep<=0:
        return estimate_board(bitboard)
    if bitboard.isFinished():
        return estimate_board(bitboard)
    if bitboard.isPass():
        bitboard.turn=1-bitboard.turn
        return -alphaBetaPruning(bitboard,deep-1,-beta,-alpha)
    legalBoard=bitboard.makeLegalBoard()
    mask=0x8000000000000000
    choose=-1
    for i in range(64):
        if legalBoard & mask:
            x=i%8
            y=i//8
            es=-alphaBetaPruning(bitboard.choose_pos_int(x,y),deep-1,False,-beta,-alpha)
            if es>alpha:
                alpha=es
                choose=i
            if alpha>=beta and (not returnAction):
                return alpha
        legalBoard<<=1
    if returnAction:
        return choose
    return alpha

def solve(bitboard):
    choose=alphaBetaPruning(bitboard,3,True)
    return 'abcdefgh'[choose%8]+str(choose//8+1)

bb=BitBoard(8)
# game loop
while True:
    lines=''
    if bb.isPass():
        print('AIはパスをしました')
        bb.turn=1-bb.turn
    else:
        s=solve(bb)
        bb=bb.choose_pos(s[0],s[1])
        print('AIが置きました')
    bb.visualize()
    a,b=map(int,input().split())
    bb=bb.choose_pos_int(a-1,b-1)
    print('あなたが起きました')
    bb.visualize()