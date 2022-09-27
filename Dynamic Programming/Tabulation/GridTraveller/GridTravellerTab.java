import java.util.Arrays;

public class GridTravellerTab
{
	public static void main(String[] args) 
	{
		int n = 3;
		int m = 3;

		int ways = gridTraveller(n, m);
		System.out.println("gridTraveller(" + m +", " + n + ") = " + ways);
	}

	public static int gridTraveller(int n, int m)
	{
		int[][] table = new int[n+1][m+1];
		int ways = 0;
		fillRow(1, 1, 1, table);
		fillCol(1, 1, 1, table);
		for(int i = 1; i < table.length; i++)
		{
			for(int j = 1; j < table[i].length; j++)
			{
				if(i+1 < table.length) table[i+1][j] += table[i][j];
				if(j+1 < table[i].length) table[i][j+1] += table[i][j];
			}
		}
		System.out.println(printTable(table));
		return table[n][m];
	}

	public static void fillRow(int value, int row, int start, int[][] table)
	{
		for(int i = start; i < table[row].length; i++)
		{
			table[row][i] = value;
		}
	}

	public static void fillCol(int value, int col, int start, int[][] table)
	{
		for(int i = start; i < table.length; i++)
		{
			table[i][col] = value;
		}
	}

	public static String printTable(int[][] table)
	{
		String str  = String.format("[\n");
		for(int i = 0; i < table.length; i++)
		{
			str += String.format("%s\n", Arrays.toString(table[i]));
		}
		str += String.format("]");

		return str;
	}
}