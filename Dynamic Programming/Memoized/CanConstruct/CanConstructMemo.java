import java.util.Arrays;
import java.util.Map;
import java.util.HashMap;
public class CanConstructMemo
{
	public static void main(String[] args) 
	{
		String target = "feeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee";
		String[] strArray = {
			"e",
			"eee",
			"eeee",
			"eeeee",
			"eeeeee",
			
		};
		Map<String, Boolean> memo = new HashMap<String, Boolean>();
		System.out.println("Can " + Arrays.toString(strArray) + " construct '" + target + "': " + canConstruct(target, strArray, memo));
		// String end = "ciple";
		// int n = end.length();
		// System.out.println("Does '" + target + "' ends with '" + end + "': " + hasEnd(target, end));
		// System.out.println("remove the last " + n + " letters from " + target + ": " + removeEnd(target, n));
		// System.out.println(target);
	}
	/**
		determine wether the strings on array can construct the target string
		@param target the target string
		@param strArray the list of string that could possibly construct the target string
		@return true if the strings on the array can construct the target string
	*/
	public static Boolean canConstruct(String target, String[] strArray, Map<String, Boolean> memo)
	{
		if(target.equals("")) return true;
		if(memo.containsKey(target)) return memo.get(target);

		for(String str : strArray)
		{
			if(hasEnd(target, str))
			{
				boolean res = canConstruct(removeEnd(target, str.length()), strArray, memo);
				if(res)
				{
					memo.put(target, true);
					return true;
				}

			}
		}
		memo.put(target, false);
		return false;
	}

	/**
		checks to see if the target string has an ending that is equal to end
		for example target = Jayvee, end = vee, then hasEnd(target, end) should return true
		@param target the string to check
		@param end the string to compare to the end of the string
		@return true if the target string has an end that is equals to the end
	*/
	public static Boolean hasEnd(String target, String end)
	{
		if(end.length() <= target.length()) return target.substring(target.length() - end.length()).equals(end);
		else return false;
	}

	/**
		removes n letters from the target string
		example: removeEnd("Jayvee", 3) = "jay"
		@param target the target string
		@param n the number of letters to remove
		@return the new string 
	*/
	public static String removeEnd(String target, int n)
	{
		if(n <= target.length()) return target.substring(0, target.length() - n);
		else return target;
	}
}