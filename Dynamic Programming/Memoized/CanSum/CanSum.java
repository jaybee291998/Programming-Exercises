import java.util.*;

public class CanSum
{
	public static void main(String[] args) 
	{
		int n = 300;
		ArrayList<Integer> array = new ArrayList<Integer>();
		array.add(7);
		array.add(14);
		//array.add(11);
		Collections.sort(array);
		boolean res = canSum(n, array);
		System.out.println("canSum(" + n + " " + array + "): " + res);
		System.out.println(res);
	}

	public static boolean canSum(int n, ArrayList<Integer> array)
	{
		if(array.contains(n)) return true;
		if(array.contains(1)) return true;
		if(n < array.get(0)) 	return false;
		for(int i : array)
		{
			if(canSum(n-i, array)) return true;
		}
		return false;
	}
}