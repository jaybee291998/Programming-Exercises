import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

public class MemoTest
{
	public static void main(String[] args) 
	{
		Map<Integer, ArrayList<Integer>> memo = new HashMap<Integer, ArrayList<Integer>>();

		for(int num = -2; num < 5; num++)
		{
			ArrayList<Integer> bestRes = null;
			for(int i = 0; i < 10; i++)
			{
				int len = (int)(Math.random()*10)+1;
				ArrayList<Integer> res = gen(num, len);
				res.add(len);
				if(bestRes == null || res.size() < bestRes.size())
				{
					bestRes = res;
				}
			}
			memo.put(num, bestRes);
		}

		System.out.println("memo = " + memo);
	}

	public static ArrayList<Integer> gen(int n, int len)
	{
		ArrayList<Integer> arr = new ArrayList<Integer>();
		for(int i = 0; i < len; i++)
		{
			arr.add(n);
		}
		return arr;
	}
}