import java.util.Scanner;
import java.util.ArrayList;

public class FibonacciMemoization
{
	public static void main(String[] args) 
	{
		Scanner in = new Scanner(System.in);
		ArrayList<Integer> memory = new ArrayList<Integer>();

		int n = 0;
		int fib = 0;

		System.out.print("n = ");
		n = in.nextInt();

		fib = fibonacci(n);
		System.out.println("fib(" + n + ") = " + fib);	
	}

	public static int fibonacci(int n)
	{
		if(n <= 2) return 1;
		return fibonacci(n-1) + fibonacci(n-2);
	}
}