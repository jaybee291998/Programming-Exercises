import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

public class BestSumMemo
{
	public static void main(String[] args) 
	{
		int n = 100;
		int[] array = {1,2,5,25};
		Map<Integer, ArrayList<Integer>> memo = new HashMap<Integer, ArrayList<Integer>>();
		// ArrayList<Integer> res = bestSum(n, array, memo);
		// System.out.println("bestSum(" + n + " " + arrayToString(array) + "): " + res);
		for(int i = 10; i < 100; i++)
		{
			ArrayList<Integer> res = bestSum(i, array, memo);
			System.out.println("bestSum(" + i + ", " + arrayToString(array) + "): " + res);
		}
		

	}

	public static ArrayList<Integer> bestSum(int n, int[] array, Map<Integer, ArrayList<Integer>> memo)
	{
		if(n == 0) return new ArrayList<Integer>();
		if(n < 0) 	return null;
		if(memo.containsKey(n)) return memo.get(n);
		
		ArrayList<Integer> bestRes = null;
		for(int num : array)
		{
			ArrayList<Integer> res = bestSum(n-num, array, memo);
			if(res != null)
			{
				res = new ArrayList<Integer>(res);
				res.add(num);
				if(bestRes == null || res.size() < bestRes.size()) 
				{
					bestRes = res;
				}
			}
		}

		memo.put(n, bestRes);
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