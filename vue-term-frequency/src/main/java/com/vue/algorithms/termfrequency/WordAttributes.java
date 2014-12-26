package com.vue.algorithms.termfrequency;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Set;

import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;

/**
 * A class that encapsulates a word string and related products.  This class holds the global frequency count of
 * a word and the product specific counts for the word.
 *
 */
public class WordAttributes implements Comparable<WordAttributes> {
	private final String mWord;
	private int mTotalCount = 0;
	/**
	 * {@link WordProductInfo} objects keyed on the product ids.
	 */
	private HashMap<String, WordProductInfo> mProductSet = new HashMap<String, WordProductInfo>();
	
	public WordAttributes(String word) {
		mWord = word;
	}
	public Set<String> getKeySet() {
		return mProductSet.keySet();
	}
	public String getWord() {
		return mWord;
	}
	
	public int getTotalCount() {
		return mTotalCount;
	}
	
	public void setTotalCount(int count) {
		mTotalCount = count;
	}

	public ArrayList<WordProductInfo> getSortedProductInfo() {
		ArrayList<WordProductInfo> productList = new ArrayList<WordProductInfo>();
		productList.addAll(mProductSet.values());
		Collections.sort(productList);
		Collections.reverse(productList);
		return productList;
	}
	/**
	 * Adds a product to this word. Meaning this word showed up in the description/title/etc of this product.
	 * @param productId The unique identifier for this product. Currently we use the url of the product.
	 * @param location The location identifies the word position in the product. The the sentence "This is a red dress"
	 * The word position of red is 3. However we also exclude stop words so 'a' and 'is' gives the word 'red' a location
	 * of 1.
	 */
	public void addProduct(String productId, int location) {
		WordProductInfo productInfo = mProductSet.get(productId);
		if (productInfo == null) {
			productInfo = new WordProductInfo(productId);
			mProductSet.put(productId, productInfo);
		}
		productInfo.addLocation(location);
		mTotalCount++;
	}
	
	public void addProductMultiLocation(String ProductId, int[] locations) {
		throw new UnsupportedOperationException("Method addProductMultiLocation is unimplemented");
	}
	
	@Override
	public int hashCode() {
		return new HashCodeBuilder(5, 13).append(mWord).toHashCode();
	}
	
	@Override
	public boolean equals(Object obj) {
		if (obj == null) { return false; }
		if (obj == this) { return true; }
		if (obj.getClass() != getClass()) {
			return false;
		}
		WordAttributes wAtt = (WordAttributes) obj;
		return new EqualsBuilder().
	            append(mWord, wAtt.mWord).
	            isEquals();
	}
	
	@Override
	public String toString() {
		return mWord + " : " + mTotalCount;
	}

	public int compareTo(WordAttributes other) {
		return mTotalCount - other.mTotalCount;
	}
}
