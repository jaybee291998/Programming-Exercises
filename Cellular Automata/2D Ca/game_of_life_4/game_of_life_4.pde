final int WIDTH = 100;
final int HEIGHT = WIDTH;

int w;

int[][] board;
double overpopulation_death_chance = 0.95;
double loneliness_death_chance = 0.30;
double probability_of_life = 0.05;

void setup()
{
  size(800, 800);
  w = (int)(height / HEIGHT);
  board = new int[WIDTH][HEIGHT];
  for(int i = 0; i < board[0].length; i++)
  {
    for(int j = 0; j < board.length; j++)
    {
      board[i][j] = Math.random() <= probability_of_life? 1 : 0;
    }
  } 
}

void draw()
{
  frameRate(60);
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
    //overpopulation
    if(aliveNeighbors >= 4)
    {
      newState = Math.random() <= overpopulation_death_chance? 0 : 1;
    }
    //loneliness
    else if(aliveNeighbors <= 1)
    {
      newState = Math.random() <= loneliness_death_chance? 0 : 1;;
    }
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
