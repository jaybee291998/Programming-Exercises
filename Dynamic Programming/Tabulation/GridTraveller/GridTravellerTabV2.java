import java.util.Arrays;
import java.util.Scanner;

public class GridTravellerTabV2
{
	public static void main(String[] args) 
	{
		Scanner in = new Scanner(System.in);

		int n = 0;
		int m = 0;

		System.out.print("n = ");
		n = in.nextInt();

		System.out.print("m = ");
		m = in.nextInt();


		int ways = gridTraveller(n, m);
		System.out.println("gridTraveller(" + m +", " + n + ") = " + ways);
	}

	public static int gridTraveller(int n, int m)
	{
		int[][] table = new int[n][m];
		int ways = 0;
		fillRow(1, 0, 0, table);
		fillCol(1, 0, 0, table);
		for(int i = 1; i < table.length; i++)
		{
			for(int j = 1; j < table[i].length; j++)
			{
				table[i][j] = table[i-1][j] + table[i][j-1];
			}
		}
		return table[n-1][m-1];
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