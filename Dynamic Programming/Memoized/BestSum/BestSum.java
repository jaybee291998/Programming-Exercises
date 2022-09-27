import java.util.ArrayList;

public class BestSum
{
	public static void main(String[] args) 
	{
		int n = 8;
		int[] array = {1,2,3,5};
		ArrayList<Integer> res = bestSum(n, array);
		System.out.println("bestSum(" + n + " " + arrayToString(array) + "): " + res);
		//System.out.println(res);
	}

	public static ArrayList<Integer> bestSum(int n, int[] array)
	{
		if(n == 0) return new ArrayList<Integer>();
		if(n < 0) 	return null;
		ArrayList<Integer> bestRes = null;
		for(int num : array)
		{
			ArrayList<Integer> res = bestSum(n-num, array);
			if(res != null)
			{
				res.add(num);
				if(bestRes == null || res.size() < bestRes.size()) 
				{
					bestRes = res;
				}
			}
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