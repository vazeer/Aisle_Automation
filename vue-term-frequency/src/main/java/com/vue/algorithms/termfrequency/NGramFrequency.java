package com.vue.algorithms.termfrequency;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;

/**
 * This class is suppose to be able to calculate the n-tuple word frequency. Currently it uses a brute force method
 * which is inefficient and is very slow for 2 word combinations and almost non functional for 3 word. If used for
 * > 3 words than a threashold value must be used if the number of words is large.
 *
 */
public class NGramFrequency {
	private ArrayList<WordAttributes> mSortedWordAttr;
	private ArrayList<WordAttributes> mNGramResult = new ArrayList<WordAttributes>();
	public final int n;
	private boolean mDebug = false;

	public NGramFrequency(int n, ArrayList<WordAttributes> sortedWordAttr) {
		if (n < 2) throw new IllegalArgumentException();
		this.n = n;
		this.mSortedWordAttr = sortedWordAttr;
	}
	
	public NGramFrequency(int n, ArrayList<WordAttributes> sortedWordAttr, double topXPercent) {
		if (n < 2) throw new IllegalArgumentException();
		this.n = n;
		keepTopNPercentWords(topXPercent, sortedWordAttr);
	}
	
	public NGramFrequency(int n, ArrayList<WordAttributes> sortedWordAttr, int topX) {
		if (n < 2) throw new IllegalArgumentException();
		this.n = n;
		keepTopN(topX, sortedWordAttr);
	}

	public void setDebug(boolean b) {
		mDebug = b;
	}
	
	public ArrayList<WordAttributes> buildNGramFrequency() {
		recursiveFor(0, n, "");
		Collections.sort(mNGramResult);
		Collections.reverse(mNGramResult);
		return mNGramResult;
	}
	
	public void recursiveFor(int start, int level, String soFar) {
		if (level == 0) {
			// remove the first ':'
			soFar = soFar.substring(1);
			String[] split = soFar.split(":");
			int result = processWords(split, soFar);
			if (result > 0) {
				WordAttributes nGramWord = new WordAttributes(soFar);
				nGramWord.setTotalCount(result);
				mNGramResult.add(nGramWord);
				if (mDebug) {
					System.out.println(nGramWord.toString());
				}
			}
			return;
		} else {
			for (int i = start; i < mSortedWordAttr.size() - n + 1; i++) {
				// we can return, not continue, because they are sorted.
				if (mSortedWordAttr.get(i).getTotalCount() < 50) return;
				String append = soFar + ":" + mSortedWordAttr.get(i).getWord();
				recursiveFor(i+1, level-1, append);
			}
		}
	}
	
	private int processWords(String[] words, String soFar) {
		WordAttributes wordAtt = getWordAttribute(words[0]);
		HashSet<String> productIds = new HashSet<String>(wordAtt.getKeySet());
		for (int i = 1; i < words.length; i++) {
			wordAtt = getWordAttribute(words[i]);
			productIds.retainAll(wordAtt.getKeySet());
		}
		if (!productIds.isEmpty()) {
			return productIds.size();
		}
		return 0;
	}
	
	private WordAttributes getWordAttribute(String word) {
		for (WordAttributes wordAttributes : mSortedWordAttr) {
			if (wordAttributes.getWord().equals(word)) return wordAttributes;
		}
		return null;
	}
	
	private void keepTopNPercentWords(double x, ArrayList<WordAttributes> sortedWordAttr) {
		keepTopN((int)(sortedWordAttr.size() * x), sortedWordAttr);
	}
	
	private void keepTopN(int x, ArrayList<WordAttributes> sortedWordAttr) {
		mSortedWordAttr = new ArrayList<WordAttributes>(sortedWordAttr.subList(0, x));
	}
}
