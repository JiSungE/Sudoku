import random

class Sudoku():  
    def __init__(self):
        # 보드 크기
        self.SIZE = 9 
        self.origin_board = [[0 for j in range(0,self.SIZE)] for i in range(0,self.SIZE)]
        # 스도쿠 2차원 board
        self.board = [[0 for j in range(0,self.SIZE)] for i in range(0,self.SIZE)]
        # 어떤 숫자들이 채워졌는지를 체크하는 row, col 2차원 리스트
        self.row = [[0 for j in range(0,self.SIZE+1)] for i in range(0,self.SIZE+1)]
        self.col = [[0 for j in range(0,self.SIZE+1)] for i in range(0,self.SIZE+1)]
        # 3 * 3 사각형에 어떤 숫자들이 채워졌는지를 체크하는 2차원 리스트 diag
        self.diag = [[0 for j in range(0,self.SIZE+1)] for i in range(0,self.SIZE+1)]
        # DFS 기반의 백트래킹을 이용하므로 단 1개의 스도쿠 퍼즐만 생성하고 종료하기 위한
        # 변수 terminate_flag
        self.terminate_flag = False
        # 클래스 멤버를 초기화 해주는 함수
        self.__board_init()

    # 클래스 멤버 초기화
    def __board_init(self):
        # 1번째, 4번째, 9번째 3*3 사각형을 미리 채워주는 역할
        seq_diag = [0,4,8]
        for offset in range(0,9,3):
            seq = [i for i in range(1,self.SIZE+1)]
            random.shuffle(seq)
            for idx in range(0,9):
                i,j = idx//3,idx%3
                self.row[offset+i][seq[idx]] = 1
                self.col[offset+j][seq[idx]] = 1
                k = seq_diag[offset//3]
                self.diag[k][seq[idx]] = 1
                self.origin_board[offset+i][offset+j] = seq[idx]

    def __clean(self):
        self.origin_board = [[0 for j in range(0,self.SIZE)] for i in range(0,self.SIZE)]
        self.board = [[0 for j in range(0,self.SIZE)] for i in range(0,self.SIZE)]
        self.row = [[0 for j in range(0,self.SIZE+1)] for i in range(0,self.SIZE+1)]
        self.col = [[0 for j in range(0,self.SIZE+1)] for i in range(0,self.SIZE+1)]
        self.diag = [[0 for j in range(0,self.SIZE+1)] for i in range(0,self.SIZE+1)]
        self.terminate_flag = False


    # 백트레킹을 이용하여, 미리 채워놓은 부분을 제외하고, 나머지 부분을 채워넣는 함수
    def __make_sudoku(self, k):

        if self.terminate_flag == True:
            return True

        board_size = self.SIZE*self.SIZE
        if k >= board_size :
            for i in range(0,self.SIZE):
                for j in range(0,self.SIZE):
                    self.board[i][j] = self.origin_board[i][j]
            self.terminate_flag = True
            return True

        i,j = k//self.SIZE,k%self.SIZE
        start_num = random.randint(1,self.SIZE)

        if self.origin_board[i][j] != 0:
            self.__make_sudoku(k+1)

        for num in range(1,self.SIZE+1):
            num = 1 + (num + start_num)%9
            d = (i//3)*3 + (j//3)
            if self.row[i][num] == 0 and self.col[j][num] == 0 and self.diag[d][num] == 0:
                self.row[i][num],self.col[j][num],self.diag[d][num] = 1,1,1
                self.origin_board[i][j] = num
                self.__make_sudoku(k+1)
                self.row[i][num],self.col[j][num],self.diag[d][num] = 0,0,0
                self.origin_board[i][j] = 0

    # 스도쿠가 정답인지 뿐만 아니라 잘못된 데이터가 들어갔는지도 같이 체크한다.
    def __sudoku_check(self, puzzle):
        if type(puzzle) != type([]) or len(puzzle) == 0:
            return False

        row_size = len(puzzle)
        col_size = min([len(puzzle[i]) for i in range(0,row_size-1)])

        if col_size != self.SIZE or row_size != self.SIZE:
            return False

        for i in range(0,self.SIZE):
            for j in range(0,self.SIZE):
                if type(puzzle[i][j]) != type(1):
                    return False

        for i in range(0,self.SIZE):
            for j in range(0,self.SIZE):
                k = (i//3)*3 + (j//3)
                num = puzzle[i][j]
                self.row[i][num]+=1
                self.col[j][num]+=1
                self.diag[k][num]+=1

        for idx in range(0,self.SIZE):
            for num in range(1,self.SIZE+1):
                if self.row[idx][num]!=1 or self.col[idx][num]!=1 or self.diag[idx][num]!=1:
                    return False

        return True

    def __generate_puzzle(self):
        self.__clean()
        self.__make_sudoku(0)
        return self.board

    def generate_sudoku(self):
        puzzle = self.__generate_puzzle()
        count = random.randint(15,40)
        remove_coords = {}
        for i in range(0,count):
            coord = random.randint(0,self.SIZE-1),random.randint(0,self.SIZE-1)
            while coord not in remove_coords:
                coord = random.randint(0,self.SIZE-1),random.randint(0,self.SIZE-1)
                remove_coords[coord] = coord

        for coord in remove_coords:
            di,dj = coord[0],coord[1]
            puzzle[di][dj] = 0
        return puzzle

    def sudoku_check(self, puzzle):
        self.__clean()
        return self.__sudoku_check(puzzle)