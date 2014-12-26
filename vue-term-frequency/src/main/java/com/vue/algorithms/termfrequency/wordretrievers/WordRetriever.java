package com.vue.algorithms.termfrequency.wordretrievers;

import java.io.File;
import java.io.IOException;
import java.util.HashSet;

import com.vue.algorithms.termfrequency.WordDescription;
import com.vue.algorithms.termfrequency.App.FileAndContent;
import com.vue.algorithms.termfrequency.wordretrievers.RetrieverBuilderFactory.RetrieverType;

/**
 * Word Retiever interface. Word retrievers are set up to be used muiltiple time for the same file type. Just make sure
 * to call the {@link WordRetriever#setup(File, HashSet, RetrieverType)} function again.
 */
public interface WordRetriever {
	/**
	 * Sets up the word retriever. This function must be called before any calls to {@link WordRetriever#nextWord()} is
	 * made.
	 * @param fContent The {@link FileAndContent} that is to be processed by this {@link WordRetriever}.
	 * @param type TODO
	 * @throws IOException
	 */
	void setup(FileAndContent fContent, HashSet<String> stopWords) throws IOException;
	/**
	 * This function must be called after a word retriever is done or no longer needed. It closes the file readers
	 * and cleans up.
	 * @throws IOException
	 */
	void close() throws IOException;
	/**
	 * Gets the next {@link WordDescription}.
	 * 
	 * @return Returns the next {@link WordDescription} in the file related to the a product description. If no more
	 * words are available null is returned.
	 * @throws IOException 
	 */
	WordDescription nextWord() throws IOException;
	
	/**
	 * Gets the associated type of this retriever.
	 * @return
	 */
	RetrieverType getRetrieverType();
	
	/**
	 * @return if this {@link WordRetriever} is ready ie can {@link WordRetriever#nextWord()} be called.
	 */
	boolean isReady();
}
