package com.vue.algorithms.termfrequency;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashSet;

import com.vue.algorithms.termfrequency.wordretrievers.RetrieverBuilderFactory;
import com.vue.algorithms.termfrequency.wordretrievers.WordRetriever;
import com.vue.algorithms.termfrequency.wordretrievers.RetrieverBuilderFactory.RetrieverType;

/**
 * This class is the main entry point for processing term frequencies in the vue
 * products.
 *
 */
public class App {

	/**
	 * This method process a single file represented by a {@link FileAndContent}
	 * object.
	 * 
	 * @param fileContent
	 *            The pointer to the file that is going to be processed.
	 * @param wordFrequencyBuilder
	 *            The builder into which all the words will be processed.
	 * @param stopWordsSet
	 *            The set of words that should be ignored.
	 * @throws IOException
	 */
	public static void processFile(FileAndContent fileContent,
			WordFrequencyBuilder wordFrequencyBuilder,
			HashSet<String> stopWordsSet) throws IOException {
		WordRetriever retriever = RetrieverBuilderFactory
				.GetRetriever(fileContent.mType);
		try {
			retriever.setup(fileContent, stopWordsSet);
			WordDescription wordDescription = retriever.nextWord();
			while (wordDescription != null) {
				if (wordDescription.word.length() < 2
						|| stopWordsSet.contains(wordDescription.word)) {
					wordDescription = retriever.nextWord();
					continue;
				}
				// Send to frequency builder.
				wordFrequencyBuilder
						.addWord(wordDescription.word,
								wordDescription.productID,
								wordDescription.wordLocation);
				wordDescription = retriever.nextWord();
			}
		} finally {
			retriever.close();
		}
	}

	/**
	 * The main loop that builds the term frequencies.
	 * 
	 * @param stopWordsFilePath
	 *            the path to the stop words file.
	 * @param fileAndContents
	 *            the set of input files represented by {@link FileAndContent}
	 *            class.
	 * @return An instance of the {@link WordFrequencyBuilder} class.
	 * @throws IOException
	 */
	public static WordFrequencyBuilder run(String stopWordsFilePath,
			FileAndContent[] fileAndContents) throws IOException {
		// get stop words
		HashSet<String> stopWordsSet = TermFrequencyUtils
				.getStopWords(stopWordsFilePath);
		WordFrequencyBuilder wordFrequencyBuilder = new WordFrequencyBuilder();
		for (FileAndContent fileContent : fileAndContents) {
			if (fileContent.exists()) {
				processFile(fileContent, wordFrequencyBuilder, stopWordsSet);
			}
		}
		return wordFrequencyBuilder;
	}

	/**
	 * A simple class that holds the File with they file type designated by the
	 * {@link RetrieverType} enum. The constructor of this class takes in as
	 * input the expected input format of the main function which is
	 * <filepath:type>. See main method for more details.
	 */
	public static class FileAndContent {
		public final RetrieverBuilderFactory.RetrieverType mType;
		public final File mFile;

		/**
		 * Parses the input string into the appropriate member fields.
		 * 
		 * @param input
		 *            should be of the format <filepath:type> where type is
		 *            defined by
		 *            {@link RetrieverBuilderFactory#stringToEnum(String)}.
		 */
		public FileAndContent(String input) {
			String[] split = input.split(":");
			mType = RetrieverBuilderFactory.stringToEnum(split[1]);
			mFile = new File(split[0]);
		}

		public boolean exists() {
			return mFile.exists();
		}
	}

	/**
	 * @param args
	 *            The args param here consists of at least 2 arguments. The
	 *            first is the file containing the stop words that will not be
	 *            tracked by the term frequency. The 2+ args are files that will
	 *            be read in containing term information. The file args are of a
	 *            specific format <filepath:type> where 'filepath' is the path
	 *            to the input file and 'type' is a string representation of the
	 *            {@link RetrieverType}. See {@link RetrieverBuilderFactory}
	 *            class for more information on what are legal inputs for
	 *            'type'. Example:
	 * 
	 *            /Users/Behrooz/VUE/stopwords_list.txt
	 *            /Users/Behrooz/tmp/express.jl:c /Users/Behrooz/tmp/nord.jl:c
	 *            /Users/Behrooz/tmp/macy.jl:c
	 */
	public static void main(String[] args) {
		
		PrintStream out = null;
		try {
			out = new PrintStream(new FileOutputStream("/home/vazeer/Desktop/term_frequency/testyoox/stats.txt"));
		} catch (FileNotFoundException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		System.setOut(out);
		
		if (args.length < 2)
			System.err.println("Wrong number of args");
		FileAndContent[] fileAndContents = new FileAndContent[args.length - 1];
		for (int i = 1; i < args.length; i++) {
			fileAndContents[i - 1] = new FileAndContent(args[i]);
		}
		WordFrequencyBuilder builder = null;
		int numWords = 0;
		try {
			long start = System.currentTimeMillis();
			builder = run(args[0], fileAndContents);
			numWords = builder.getNumWords();
			System.out
					.println("Total time to proccess single word combination and total words ="
							+ numWords
							+ " is"
							+ (System.currentTimeMillis() - start));
			builder.print();
		} catch (IOException e) {
			e.printStackTrace();
		}
		NGramFrequency ngram = new NGramFrequency(2,
				builder.getSortedWordAttributes());
		long start = System.currentTimeMillis();
		ArrayList<WordAttributes> result = ngram.buildNGramFrequency();
		System.out
				.println("Total time to proccess double word combination and total words ="
						+ numWords
						+ " is"
						+ (System.currentTimeMillis() - start));
		for (WordAttributes wordAttributes : result) {
			System.out.println(wordAttributes.toString());
		}
		ngram = new NGramFrequency(3, builder.getSortedWordAttributes(), 75);
		start = System.currentTimeMillis();
		result = ngram.buildNGramFrequency();
		System.out
				.println("Total time to proccess triple word combination and total words ="
						+ numWords
						+ " is"
						+ (System.currentTimeMillis() - start));
		for (WordAttributes wordAttributes : result) {
			System.out.println(wordAttributes.toString());
		}
		// TODO(oddjob): write the result of the builder out to a file.
		// Gson gson = new Gson();
		// gson.toJson(builder);
		System.out.println("Done Processing!");
	}

}
