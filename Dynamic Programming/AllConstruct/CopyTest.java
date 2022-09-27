import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

public class CopyTest
{
	public static void main(String[] args) 
	{
		ArrayList<String> prin1 = new ArrayList<String>();
		prin1.add("pr"); prin1.add("in"); 

		ArrayList<String> prin2 = new ArrayList<String>();
		prin2.add("pri"); prin2.add("n");

		ArrayList<String> ciple1 = new ArrayList<String>();
		ciple1.add("ci"); ciple1.add("ple"); 

		ArrayList<String> ciple2 = new ArrayList<String>();
		ciple2.add("cip"); ciple2.add("le");

		// System.out.println("prin1: " + prin1);
		// System.out.println("prin2: " + prin2);
		// System.out.println("ciple1: " + ciple1);
		// System.out.println("ciple2: " + ciple2);

		ArrayList<ArrayList<String>> prin = new ArrayList<ArrayList<String>>();
		prin.add(prin1); prin.add(prin2);

		ArrayList<ArrayList<String>> ciple = new ArrayList<ArrayList<String>>();
		ciple.add(ciple1); ciple.add(ciple2);

		Map<String, ArrayList<ArrayList<String>>> combination = new HashMap<String, ArrayList<ArrayList<String>>>();
		combination.put("prin", prin);
		combination.put("ciple", ciple);

		
		
		
		Map<String, ArrayList<ArrayList<String>>> combinationCopy = new HashMap<String, ArrayList<ArrayList<String>>>(combination);
		ciple1.add("fuck");
		combinationCopy.put("asshat", ciple);
		System.out.println("combination: " + combination);
		System.out.println("combination copy: " + combinationCopy);

		// System.out.println("ciple: " + ciple);
		// System.out.println("prin: " + prin);

	}
}