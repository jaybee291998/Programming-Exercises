import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

public class AllConstructMemoV2
{
	public static void main(String[] args) 
	{
		String target = "eeeeeeeeeeeeeeeeeeeeeeeeee";
		String[] wordBank = {"eee", "eeee", "eeeee"};
		Map<String, ArrayList<ArrayList<String>>> memo = new HashMap<String, ArrayList<ArrayList<String>>>();
		ArrayList<ArrayList<String>> res = allConstruct(target, wordBank, memo);
		System.out.println(res.size());
		// System.out.println(memo);
	}

	/**
		find all the possible ways to construct the target string using the combination of string
		that is stored on the wordBank
		@param target the target string to be constructed
		@param wordBank stores the strings that can be used to construct the target
		@return all the possible combination of strings from the word bank to construct the target
	*/
	public static ArrayList<ArrayList<String>> allConstruct(String target, String[] wordBank, Map<String, ArrayList<ArrayList<String>>> memo)
	{
		if(target.equals(""))
		{
			ArrayList<ArrayList<String>> e = new ArrayList<ArrayList<String>>();
			e.add(new ArrayList<String>());
			return e;
		}
		if(memo.containsKey(target)) return memo.get(target);

		ArrayList<ArrayList<String>> allCombination = new ArrayList<ArrayList<String>>();
		for(String str : wordBank)
		{
			if(hasEnd(target, str))
			{
				String newTarget = removeEnd(target, str.length());
				ArrayList<ArrayList<String>> com = createCopy(allConstruct(newTarget, wordBank, memo));
				for(int i = 0; i < com.size(); i++)
				{
					com.get(i).add(str); //add the current str to all the possible combination of newTarget;
				}

				//add the contents of com to allCombination
				concatAL(com, allCombination);
			}
		}
		memo.put(target, allCombination);
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

	/**
		create a copy of the object ArrayList-ArrayList-String--- called table
		@param table to copy
		@return a copy of the table
	*/
	public static ArrayList<ArrayList<String>> createCopy(ArrayList<ArrayList<String>> table)
	{
		ArrayList<ArrayList<String>> tableCopy = new ArrayList<ArrayList<String>>();

		for(ArrayList<String> row : table)
		{
			ArrayList<String> rowCopy = new ArrayList<String>(row);
			tableCopy.add(rowCopy);
		}
		return tableCopy;
	}
}