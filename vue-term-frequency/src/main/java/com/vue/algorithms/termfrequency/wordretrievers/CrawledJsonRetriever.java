package com.vue.algorithms.termfrequency.wordretrievers;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashSet;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.vue.algorithms.termfrequency.App.FileAndContent;
import com.vue.algorithms.termfrequency.TermFrequencyUtils;
import com.vue.algorithms.termfrequency.WordDescription;
import com.vue.algorithms.termfrequency.wordretrievers.RetrieverBuilderFactory.RetrieverType;

/**
 * This word retriever specifically is able to deal with the json files that are crawled by the VUE crawlers.
 *
 */
public class CrawledJsonRetriever implements WordRetriever {
	public static final RetrieverType TYPE = RetrieverType.CRAWLED_JSON;
	private BufferedReader mReader = null;
	private String[] mCurrentWords = null;
	private int mIndex = 0;
	private int mWordLocation = 0;
	private String mCurrentProductId;
	private boolean mIsReady = false;
	private HashSet<String> mStopWords;

	public void setup(FileAndContent f, HashSet<String> stopWords) throws IOException {
		if (mReader != null) {
			mReader.close();
		}
		if (f.mType != TYPE) {
			close();
			throw new IllegalArgumentException();
		}
		mReader = new BufferedReader(new InputStreamReader(new FileInputStream(f.mFile)));
		mStopWords = stopWords;
		mIndex = 0;
		mWordLocation = 0;
		mIsReady = true;
	}

	public void close() throws IOException {
		if (mReader != null) {
			mReader.close();
		}
		mStopWords = null;
		mIndex = 0;
		mWordLocation = 0;
		mReader = null;
		mIsReady = false;
	}

	public WordDescription nextWord() throws IOException {
		if (!mIsReady) return null;
		String nextWord = getNextWord();
		while (mStopWords.contains(nextWord)) {
			nextWord = getNextWord();
		}
		if (nextWord == null) return null;
		return new WordDescription(nextWord, mCurrentProductId, mWordLocation++);
	}
	
	/**
	 * Gets the next available word. Returns null if there are no more words.
	 * @return The next word or null if no more words.
	 * @throws IOException
	 */
	private String getNextWord() throws IOException {
		if (mCurrentWords == null || mIndex >= mCurrentWords.length) {
			mIndex = 0;
			mWordLocation = 0;
			String line = mReader.readLine();
			if (line != null) {
				JSONObject jsonObj = TermFrequencyUtils.ParseJson(line);
				String appendedDescription = "";
				String productId = null;
				if (jsonObj.get("product_url") != null) {
					productId = jsonObj.get("product_url").toString();
					mCurrentProductId = productId;
				}
				if (jsonObj.get("product_title") != null) {
					appendedDescription = jsonObj.get("product_title").toString();
				}
				if (jsonObj.get("description") != null) {
					JSONArray jsonArray = (JSONArray) jsonObj.get("description");
					for (Object o : jsonArray) {
						appendedDescription += " " + o.toString();
					}
				}
				// remove all punctuation
				mCurrentWords = appendedDescription.replaceAll("[^a-zA-Z ]", " ")
						.toLowerCase().split("\\s+");
				return mCurrentWords[mIndex++];
			} else {
				return null;
			}
		}
		return mCurrentWords[mIndex++];
	}

	public RetrieverType getRetrieverType() {
		return TYPE;
	}

	public boolean isReady() {
		return mIsReady;
	}
	
}
