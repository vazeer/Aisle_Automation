package com.vue.algorithms.termfrequency.wordretrievers;

/**
 * Factory class that build {@link WordRetriever}.
 * @author oddjob
 *
 */
public class RetrieverBuilderFactory {
	public enum RetrieverType {
		UNKNOWN,
	    CRAWLED_JSON
	}
	
	public static RetrieverType stringToEnum(String s) {
		if (s.equals("c") || s.equals("crawled"))
			return RetrieverType.CRAWLED_JSON;
		return RetrieverType.UNKNOWN;
	}

	public static WordRetriever GetRetriever(RetrieverType type) {
		switch (type) {
		case CRAWLED_JSON:
			return new CrawledJsonRetriever();
		default:
			return null;
		}
	}
}
