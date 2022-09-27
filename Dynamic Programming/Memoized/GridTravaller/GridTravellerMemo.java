public class GridTravllerMemo
{
	public static void main(String[] args) 
	{
		int m = 3;
		int n = 3;
		double[][] memo = new double[m][n];
		System.out.println(gridTraveller(m, n, memo));
	}

	public static double gridTraveller(int m, int n, double[][] memo)
	{
		if(m == 0 || n == 0) return 0;
		if(m == 1 || n == 1) return 1;
		if(memo[m-1][n-1] != 0) return memo[m-1][n-1];
		if(m-1<memo[0].length && n-1<memo.length) if(memo[n-1][m-1] != 0) return memo[n-1][m-1];
		
		memo[m-1][n-1] = gridTraveller(m, n-1, memo) + gridTraveller(m-1, n, memo);
		return memo[m-1][n-1];

	}
}