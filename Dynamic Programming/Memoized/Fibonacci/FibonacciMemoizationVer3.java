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
		if(memo[n] != 0)
		{
			return memo[n];
		}
		else
		{
			memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo);
			return memo[n];
		}
	}
}