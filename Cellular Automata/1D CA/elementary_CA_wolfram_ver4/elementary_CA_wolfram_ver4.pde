final int  CELL_AMOUNT = 100;
final int RULE_SIZE = 8;
int MAX_GEN;

int[] cells = new int[CELL_AMOUNT];
int[] ruleset = new int[RULE_SIZE];
int gen;

void setup()
{
  size(1500, 1000);
  gen = 0;
  MAX_GEN = height / (width / cells.length);
  
  //set all the cells to 0
  for (int i = 0; i < cells.length; i++)
  {
    cells[i] = (int)(Math.round(Math.random()));
  }
  for(int i = 0; i < ruleset.length; i++)
  {
    ruleset[i] = (int)(Math.round(Math.random()));
  }
}

void draw()
{
  frameRate(60);
  //background(220);
  if (gen < MAX_GEN)
  {
    update_states();
    draw_cells(gen);
    gen++;
  }
  println(gen);
}

/**
 draw each cells on the screen
 @param gen
 */
void draw_cells(int gen)
{
  int side_len = width / cells.length;
  for (int i = 0; i < cells.length; i++)
  {
    if (cells[i] == 0) fill(255);
    else fill(0);
    stroke(0);
    circle(i*side_len, gen*side_len, side_len);
  }
}

/**
 updates the states of the cells
 */
void update_states()
{
  int[] new_cells = new int[cells.length];
  for (int i = 0; i < cells.length; i++)
  {
    new_cells[i] = cal_state(i);
  }

  cells = new_cells;
}

/**
 calculate the new state of the cell based on its neighbors
 @param cell
 @return the new state of the cell
 */
int cal_state(int cell)
{
  //check wether the cell is on either edge of the grid
  if (cell == 0 || cell == cells.length -  1) return cells[cell]; //return the same state
  else
  {
    int left_cell = cells[cell - 1];
    int middle_cell = cells[cell];
    int rigth_cell = cells[cell + 1];

    int new_state = rules(left_cell, middle_cell, rigth_cell);
    return new_state;
  }
}

/**
 check the ruleset for the given neighbors
 @param left
 @param middle
 @param rigth
 @return result
 */
int rules(int left, int middle, int rigth)
{
  String s = "" + left + middle + rigth;
  int index = Integer.parseInt(s,2);

  return ruleset[index];
}
