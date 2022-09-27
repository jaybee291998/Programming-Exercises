import java.util.Map;
import java.util.HashMap;

public class CanSumMemo
{
	public static void main(String[] args) 
	{
		int n = 10000;
		int[] array = {7, 14};
		Map<Integer, Boolean> memo = new HashMap<Integer, Boolean>();
		boolean res = canSum(n, array, memo);
		System.out.println("canSum(" + n + " " + arrayToString(array) + "): " + res);
		System.out.println(res);

		for(int i = 0; i < 100; i++)
		{
			res = canSum(i*22, array, memo);
			System.out.println("canSum(" + i*22 + " " + arrayToString(array) + "): " + res);
		}


		

	}

	public static boolean canSum(int n, int[] array, Map<Integer, Boolean> memo)
	{
		if(n == 0) return true;
		if(n < 0) 	return false;
		if(memo.get(n) != null) return memo.get(n);
		for(int i : array)
		{
			if(canSum(n-i, array, memo))
			{
				memo.put(n, true);
				return true;
			}
		}
		memo.put(n, false);
		return false;
	}

	public static String arrayToString(int[] array)
	{
		String str = "[";
		for(int i : array)
		{
			str += i + ", ";
		}
		str += "]";
		return str;
	}
}