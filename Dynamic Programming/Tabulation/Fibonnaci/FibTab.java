import java.util.Arrays;

public class FibTab
{
	public static void main(String[] args) 
	{
		int n = 20;
		System.out.println("fib(" + n + ") = " + fib(n)); 
	}

	public static int fib(int n)
	{
		int[] table = new int[n+1];
		table[1] = 1;
		for(int i = 0; i < n; i++)
		{
			if(i+2 <= n)
			{
				table[i+1] += table[i];
				table[i+2] += table[i];
			}
			else table[i+1] += table[i];
		}

		return table[n];
	}
}