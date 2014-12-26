package com.vue.algorithms.termfrequency;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

/**
 * The main class that processes the words and related products.
 *
 */
public class WordFrequencyBuilder {
	private HashMap<String, WordAttributes> mWordMap = new HashMap<String, WordAttributes>();
	public void addWord(String word, String productId, int location) {
		if (productId == null) return;
		WordAttributes wordAtt = mWordMap.get(word);
		if (wordAtt == null) {
			wordAtt = new WordAttributes(word);
			mWordMap.put(word, wordAtt);
		}
		wordAtt.addProduct(productId, location);
	}
	
	public WordAttributes getWordAttribute(String word) {
		return mWordMap.get(word);
	}
	
	public int getNumWords() {
		return mWordMap.size();
	}
	/**
	 * Returns a list of WordAttributes sorted by the term frequencies in descending order.
	 * @return
	 */
	public ArrayList<WordAttributes> getSortedWordAttributes() {
		ArrayList<WordAttributes> sortedAttributes = new ArrayList<WordAttributes>();
		sortedAttributes.addAll(mWordMap.values());
		Collections.sort(sortedAttributes);
		Collections.reverse(sortedAttributes);
		return sortedAttributes;
	}
	
	/**
	 * Prints out the words and frequencies.
	 */
	public void print() {
		ValueComparator bvc =  new ValueComparator(mWordMap);
        TreeMap<String,WordAttributes> sorted_map = new TreeMap<String,WordAttributes>(bvc);
        sorted_map.putAll(mWordMap);
        System.out.println("results: "+sorted_map);
        ArrayList<WordAttributes> sorted = getSortedWordAttributes();
        for (WordAttributes att : sorted) {
        	System.out.println(att.toString());
        }
	}
	
	public static class ValueComparator implements Comparator<String> {

	    Map<String, WordAttributes> base;
	    public ValueComparator(Map<String, WordAttributes> base) {
	        this.base = base;
	    }

	    // Note: this comparator imposes orderings that are inconsistent with equals.    
	    public int compare(String a, String b) {
	        return base.get(b).compareTo(base.get(a));
	    }
	}
}
