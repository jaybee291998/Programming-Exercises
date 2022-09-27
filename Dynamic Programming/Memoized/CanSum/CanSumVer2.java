import java.util.*;

public class CanSumVer2
{
	public static void main(String[] args) 
	{
		int n = 31;
		int[] array = {7, 14};
		boolean res = canSum(n, array);
		System.out.println("canSum(" + n + " " + array + "): " + res);
		System.out.println(res);
	}

	public static boolean canSum(int n, int[] array)
	{
		if(n == 0) return true;
		if(n < 0) 	return false;
		for(int i : array)
		{
			if(canSum(n-i, array)) return true;
		}
		return false;
	}
}