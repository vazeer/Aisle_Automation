package com.vue.algorithms.termfrequency;

/**
 * Simple class describing information about a word.
 *
 */
public class WordDescription {
	public final String word;
	public final String productID;
	public final int wordLocation;
	public WordDescription(String word, String productId, int wordLocation) {
		this.word = word;
		this.productID = productId;
		this.wordLocation = wordLocation;
	}
}
