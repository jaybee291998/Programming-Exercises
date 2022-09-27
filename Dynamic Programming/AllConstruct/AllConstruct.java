import java.util.ArrayList;

public class AllConstruct
{
	public static void main(String[] args) 
	{
		String target = "abcdef";
		String[] wordBank = {"ab", "abc", "cd", "def", "abcd", "ef", "c"};
		ArrayList<ArrayList<String>> res = allConstruct(target, wordBank);
		System.out.println(res);
	}

	/**
		find all the possible ways to construct the target string using the combination of string
		that is stored on the wordBank
		@param target the target string to be constructed
		@param wordBank stores the strings that can be used to construct the target
		@return all the possible combination of strings from the word bank to construct the target
	*/
	public static ArrayList<ArrayList<String>> allConstruct(String target, String[] wordBank)
	{
		if(target.equals(""))
		{
			ArrayList<ArrayList<String>> e = new ArrayList<ArrayList<String>>();
			e.add(new ArrayList<String>());
			return e;
		}

		ArrayList<ArrayList<String>> allCombination = new ArrayList<ArrayList<String>>();
		for(String str : wordBank)
		{
			if(hasEnd(target, str))
			{
				String newTarget = removeEnd(target, str.length());
				ArrayList<ArrayList<String>> com = new ArrayList<ArrayList<String>>(allConstruct(newTarget, wordBank));
				for(int i = 0; i < com.size(); i++)
				{
					com.get(i).add(str); //add the current str to all the possible combination of newTarget;
				}

				//add the contents of com to allCombination
				concatAL(com, allCombination);
			}
		}

		return allCombination;
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

	/**
		combine all the inner elements of a nested arraylist of string to another nested arraylist of string
		@param arraySrc the array to be copied into the arrayDes
		@param arrayDes the destination of the elements of arraySrc
	*/
	public static void concatAL(ArrayList<ArrayList<String>> arraySrc, ArrayList<ArrayList<String>> arrayDes)
	{
		for(ArrayList<String> arrayStr : arraySrc)
		{
			arrayDes.add(arrayStr);
		}
	}
}