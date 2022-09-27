import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

public class AllConstructMemo
{
	public static void main(String[] args) 
	{
		String target = "principle";
		String[] wordBank = {"pri", "n", "pr", "in", "ci", "ple", "cip", "le"};
		Map<String, ArrayList<ArrayList<String>>> memo = new HashMap<String, ArrayList<ArrayList<String>>>();
		ArrayList<ArrayList<String>> res = allConstruct(target, wordBank, memo);
		System.out.println(res);
		//System.out.println("Memo: " + memo);
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
		// if(memo.containsKey(target)) 
		// {
		// 	// System.out.println("Target: " + target);
		// 	// System.out.println("Combination: " + memo.get(target));
		// 	return memo.get(target);
		// }

		ArrayList<ArrayList<String>> allCombination = new ArrayList<ArrayList<String>>();
		for(String str : wordBank)
		{
			if(hasEnd(target, str))
			{
				String newTarget = removeEnd(target, str.length());
				ArrayList<ArrayList<String>> com = new ArrayList<ArrayList<String>>(allConstruct(newTarget, wordBank, memo));
				//if(newTarget.equals("prin")) System.out.println("Prin: " + com);
				for(int i = 0; i < com.size(); i++)
				{
					com.get(i).add(str); //add the current str to all the possible combination of newTarget;
				}

				//add the contents of com to allCombination
				concatAL(com, allCombination);
			}
		}
		System.out.println("Target: " + target);
		// System.out.println("Memo: " + memo);
		//System.out.println("AllCombination: " + allCombination);
		
		// if(target.equals("prin")) System.out.println("AllCombination: " + allCombination);
		memo.put(target, allCombination);
		System.out.println("Memo[" + target + "] = " + memo.get(target));
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