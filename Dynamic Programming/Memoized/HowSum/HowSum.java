import java.util.ArrayList;

public class HowSum
{
	public static void main(String[] args) 
	{
		int n = 1649;
		int[] array = {5, 10, 20, 100, 200, 500, 1000};
		ArrayList<Integer> res = howSum(n, array);
		System.out.println("canSum(" + n + " " + arrayToString(array) + "): " + res);
		//System.out.println(res);
	}

	public static ArrayList<Integer> howSum(int n, int[] array)
	{
		if(n == 0) return new ArrayList<Integer>();
		if(n < 0) 	return null;
		for(int i = 0; i < array.length; i++)
		{
			ArrayList<Integer> res = howSum(n-array[i], array);
			if(res != null)
			{
				res.add(array[i]);
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