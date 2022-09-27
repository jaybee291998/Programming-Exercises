import java.util.Scanner;

public class FibonacciMemoization
{
	public static void main(String[] args) 
	{
		Scanner in = new Scanner(System.in);

		int n = 0;
		double fib = 0;

		System.out.print("n = ");
		n = in.nextInt();

		double[] memory = new double[n + 1];

		fib = fibonacci(n, memory);
		System.out.println("fib(" + n + ") = " + fib);	
	}

	public static double fibonacci(int n, double[] memo)
	{
		if(n <= 2) return 1;
		double val;
		if(memo[n-1] != 0 && memo[n-2] != 0)
		{
			val = memo[n-1] + memo[n-2];
			memo[n] = val;
			return val;
		} 
		else if(memo[n-1] != 0 && memo[n-2] == 0)
		{
			val = memo[n-1] + fibonacci(n-2, memo);
			memo[n] = val;
			return val;
		} 
		else if(memo[n-1] == 0 && memo[n-2] != 0)
		{
			val = fibonacci(n-1, memo) + memo[n-2];
			memo[n] = val;
			return val;
		} 
		else
		{
			val = fibonacci(n-1, memo) + fibonacci(n-2, memo);
			memo[n] = val;
			return val;
		} 
	}
}