import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

public class BestSumMemo
{
	public static void main(String[] args) 
	{
		int n = 8;
		int[] array = {2,3,5};
		ArrayList<Integer>[] memo = new ArrayList<Integer>[n];
		ArrayList<Integer> res = bestSum(n, array, memo);
		System.out.println("bestSum(" + n + " " + arrayToString(array) + "): " + res);

		System.out.println(memo);
		//System.out.println(res);
	}

	public static ArrayList<Integer> bestSum(int n, int[] array, ArrayList<Integer>[] memo)
	{
		if(n == 0) return new ArrayList<Integer>();
		if(n < 0) 	return null;
		if(memo[n]) return memo.get(n);
		ArrayList<Integer> bestRes = null;
		for(int num : array)
		{
			ArrayList<Integer> res = bestSum(n-num, array, memo);
			if(res != null)
			{
				res.add(num);
				if(bestRes == null || res.size() < bestRes.size()) 
				{
					bestRes = res;
				}
			}
		}
		System.out.println(n + " = " + bestRes);
		if(!memo.containsKey(n))
		{
			memo.put(n, bestRes);
		}
		
		return bestRes;
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