import java.util.ArrayList;

public class HowSumVer2
{
	public static void main(String[] args) 
	{
		int n = 18;
		int[] array = {5, 10, 20, 100, 200, 500, 1000, 1};
		ArrayList<Integer> res = howSum(n, array);
		System.out.println("canSum(" + n + " " + arrayToString(array) + "): " + res);
		//System.out.println(res);
	}

	public static ArrayList<Integer> howSum(int n, int[] array)
	{
		if(n == 0) return new ArrayList<Integer>();
		if(n < 0) 	return null;
		for(int num : array)
		{
			ArrayList<Integer> res = howSum(n-num, array);
			if(res != null)
			{
				res.add(num);
				return res;
			}
		}
		return null;
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