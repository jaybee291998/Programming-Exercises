import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.Scanner;

public class HowSumMemoDebug
{
	public static void main(String[] args) 
	{
		Scanner in = new Scanner(System.in);
		int n = 7;
		int[] array = {7,3,11,13};
		Map<Integer, ArrayList<Integer>> memo = new HashMap<Integer, ArrayList<Integer>>();

		System.out.print("n= ");
		n = in.nextInt();
		ArrayList<Integer> res = howSum(n, array, memo);
		System.out.println("howSum(" + n + " " + arrayToString(array) + "): " + res);
		//System.out.println(res);
	}

	public static ArrayList<Integer> howSum(int n, int[] array, Map<Integer, ArrayList<Integer>> memo)
	{
		if(n == 0) return new ArrayList<Integer>();
		if(n < 0) 	return null;
		if(memo.containsKey(n))
		{
			System.out.println("memo(" + n + ") is used");
			return memo.get(n);
		} 
		for(int num : array)
		{
			ArrayList<Integer> res = howSum(n-num, array, memo);
			if(res != null)
			{
				res.add(num);
				memo.put(n, res);
				//System.out.println("howSum(" + n + ") = " + res);
				//System.out.println("memo = " + memo);
				return res;
			}
		}
		//System.out.println("memo = " + memo);
		memo.put(n ,null);
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