final int WIDTH = 800;
final int HEIGHT = WIDTH;

int w;

int[][] board;

void setup()
{
  size(2000, 2000);
  w = (int)(height / HEIGHT);
  board = new int[WIDTH][HEIGHT];
  for(int i = 0; i < board[0].length; i++)
  {
    for(int j = 0; j < board.length; j++)
    {
      board[i][j] = (int)(random(2));
    }
  } 
}

void draw()
{
  frameRate(30);
  background(220);
  drawBoard();
  updateBoard();
}

void updateBoard()
{
  int[][] newBoard = new int[WIDTH][HEIGHT];
  for(int i = 0; i < newBoard[0].length; i++)
  {
    for(int j = 0; j < newBoard.length; j++)
    {
      newBoard[i][j] = rule(i, j);
    }
  } 
  board = newBoard;
}

int rule(int x, int y)
{  
  int aliveNeighbors = getAliveNeighbors(x, y);
  int state = board[x][y];
  int newState = 0;
  //death
  if(state == 1)
  {
    if(aliveNeighbors >= 4) newState = 0;
    else if(aliveNeighbors <= 1) newState = 0;
    else newState = 1;
  }
  else //birth
  {
    if(aliveNeighbors ==3 ) newState = 1;
    else if(aliveNeighbors != 3) newState = 0;
  }
  return newState;
}

void drawBoard()
{
  for(int i = 0; i < board[0].length; i++)
  {
    for(int j = 0; j < board.length; j++)
    {
      if(board[i][j] == 1) fill(0);
      else fill(255);
      stroke(0);
      rect(i*w, j*w, w, w);
    }
  } 
}

int getAliveNeighbors(int x, int y)
{
  int aliveNeighbors = 0;
  for(int i = -1; i < 2; i++)
  {
    for(int j = -1; j < 2; j++)
    {
       int nX = x + i; int nY = y + j;
       if((nX > 0 && nX < board[0].length) && (nY > 0 && nY < board.length))
       {
         aliveNeighbors += board[nX][nY];
       }
    }
  }
  aliveNeighbors -= board[x][y];
  return aliveNeighbors;
}
