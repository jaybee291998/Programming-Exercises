public class GridTravller
{
	public static void main(String[] args) 
	{
		System.out.println(gridTraveller(18, 18));
	}

	public static double gridTraveller(int m, int n)
	{
		if(m == 0 || n == 0) return 0;
		if(m == 1 || n == 1) return 1;
		return gridTraveller(m, n-1) + gridTraveller(m-1, n);

	}
}