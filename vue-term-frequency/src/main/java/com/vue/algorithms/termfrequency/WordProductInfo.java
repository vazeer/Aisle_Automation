package com.vue.algorithms.termfrequency;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;

/**
 * This class holds the product specific information for a word.
 *
 */
public class WordProductInfo implements Comparable<WordProductInfo>{
	private final String mProductUID;
	private ArrayList<Integer> mLocations = new ArrayList<Integer>();
	private int mOccuranceCount = 0;
	
	public WordProductInfo(String productID) {
		mProductUID = productID;
	}

	public List<Integer> getLocationList() {
		return Collections.unmodifiableList(mLocations);
	}
	
	public int getmOccuranceCount() {
		return mOccuranceCount;
	}

	public void setmOccuranceCount(int mOccuranceCount) {
		this.mOccuranceCount = mOccuranceCount;
	}
	
	public boolean addLocation(int location) {
		if (mLocations.contains(location)) return false;
		mOccuranceCount++;
		mLocations.add(location);
		return true;
	}
	
	public String getmProductUID() {
		return mProductUID;
	}
	
	@Override
	public int hashCode() {
		return new HashCodeBuilder(17, 37).
				append(mProductUID).
				toHashCode();
	}
	
	@Override
	public boolean equals(Object obj) {
		if (obj == null) { return false; }
		if (obj == this) { return true; }
		if (obj.getClass() != getClass()) {
			return false;
		}
		WordProductInfo wpi = (WordProductInfo) obj;
		return new EqualsBuilder().
	            append(mProductUID, wpi.mProductUID).
	            isEquals();
	}

	public int compareTo(WordProductInfo o) {
		return mOccuranceCount - o.mOccuranceCount;
	}
}
