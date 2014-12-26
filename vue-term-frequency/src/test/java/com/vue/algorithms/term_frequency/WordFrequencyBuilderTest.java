package com.vue.algorithms.term_frequency;

import static org.junit.Assert.*;

import java.io.IOException;
import java.util.ArrayList;

import org.junit.Before;
import org.junit.Test;

import com.vue.algorithms.termfrequency.WordAttributes;
import com.vue.algorithms.termfrequency.WordFrequencyBuilder;
import com.vue.algorithms.termfrequency.WordProductInfo;

public class WordFrequencyBuilderTest {
	private WordFrequencyBuilder mBuilder;
	
	@Before
	public void setUp() throws Exception {
		mBuilder = new WordFrequencyBuilder();
	}
	@Test
	public void testAddWordSimple() throws IOException {
		mBuilder.addWord("foo", "http://foo.com", 1);
		mBuilder.addWord("foo", "http://bar.com", 2);
		mBuilder.addWord("foo", "http://bar.com", 3);
		mBuilder.addWord("foo", "http://baz.com", 3);
		mBuilder.addWord("foo", "http://baz.com", 4);
		mBuilder.addWord("foo", "http://baz.com", 5);
		final WordAttributes att = mBuilder.getWordAttribute("foo");
		assertNotNull(att);
		assertEquals(6, att.getTotalCount());
		assertEquals("foo", att.getWord());
		ArrayList<WordProductInfo> sortedProductList = att.getSortedProductInfo();
		assertEquals(3, sortedProductList.size());
		WordProductInfo wordPInfo = sortedProductList.get(0);
		assertEquals(3, wordPInfo.getmOccuranceCount());
		assertEquals("http://baz.com", wordPInfo.getmProductUID());
		wordPInfo = sortedProductList.get(1);
		assertEquals(2, wordPInfo.getmOccuranceCount());
		assertEquals("http://bar.com", wordPInfo.getmProductUID());
		wordPInfo = sortedProductList.get(2);
		assertEquals(1, wordPInfo.getmOccuranceCount());
		assertEquals("http://foo.com", wordPInfo.getmProductUID());
	}	
}
