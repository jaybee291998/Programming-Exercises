import java.util.Arrays;
public class CountConstruct
{
	public static void main(String[] args) 
	{
		String target = "ffeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee";
		String[] wordBank = {"e", "ee", "eee", "eeee", "eeeee", "eeeeee"};	
		int countWays = countConstruct(target, wordBank);
		System.out.println("There are " + countWays + " ways to construct the target string '" + target +"' from the word bank " + Arrays.toString(wordBank));
	}

	/**
		count how many ways can the target be constructed using the strings on the word bank
		@param target the target string
		@param wordBank the list of string that can be used to cinstrut the target 
		@return the count of ways to construct the target
	*/
	public static int countConstruct(String target, String[] wordBank)
	{
		if(target.equals("")) return 1;
		int count = 0;

		for(String str : wordBank)
		{
			if(hasEnd(target, str))
			{
				String newTarget = removeEnd(target, str.length());
				count += countConstruct(newTarget, wordBank);
			}
		}
		return count;
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