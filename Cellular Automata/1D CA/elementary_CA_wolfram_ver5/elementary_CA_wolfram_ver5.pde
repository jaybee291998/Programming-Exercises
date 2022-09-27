import java.util.LinkedList;
import java.util.ListIterator;

final int  CELL_AMOUNT = 200;
int MAX_GEN;
int curGen;

int[] cells = new int[CELL_AMOUNT];
int[] ruleset = {0, 1, 0, 1, 1, 0, 1, 0};
LinkedList<int[]> cells_stack;
void setup()
{
  size(1500, 1000);
  curGen= 0;
  MAX_GEN = height / (width / cells.length);
  cells_stack = new LinkedList<int[]>();
  
  //set all the cells to 0
  for (int i = 0; i < cells.length; i++)
  {
    cells[i] = 0;
  }
  int mid= (int)(cells.length/2);
  cells[mid] = 1;
}

void draw()
{
  frameRate(60);
  //background(220);
  //if (curGen < MAX_GEN)
  //{
    update_states();
    draw_cells();
    curGen++;
  //}
  println(curGen);
}

/**
 draw each cells on the screen
 @param gen
 */
void draw_cells()
{
  ListIterator<int[]> csIter = cells_stack.listIterator();
  int side_len = width / cells.length;
  int curCells_index = 0;
  while(csIter.hasNext())
  {
    int[] current_cells = csIter.next();
    for (int i = 0; i < current_cells.length; i++)
    {
      if (current_cells[i] == 0) fill(255);
      else fill(0);
      stroke(0);
      rect(i*side_len, curCells_index*side_len, side_len, side_len);
    }
    curCells_index++;
  }
  if(curGen > MAX_GEN) cells_stack.removeFirst();

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
  cells_stack.addLast(cells);
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
