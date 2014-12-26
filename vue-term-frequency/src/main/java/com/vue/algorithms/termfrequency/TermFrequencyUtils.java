package com.vue.algorithms.termfrequency;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashSet;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

/**
 * A set of utility function that are used by the term frequency pipeline.
 *
 */
public class TermFrequencyUtils {
	private static final JSONParser mParser = new JSONParser();
	/**
	 * A simple file reader that reads in the stop words file where each word is represented on a seperate line of the
	 * file. This method is just a wrapper around the {@link TermFrequencyUtils#readStopWords(File, HashSet)} function.
	 * @param stopWordsFilePath The path to the file.
	 * @return a {@link HashSet} of all the words that should be ignored.
	 * @throws IOException
	 */
	public static HashSet<String> getStopWords(String stopWordsFilePath) throws IOException {
		File stopWordFile = new File(stopWordsFilePath);
		if (!stopWordFile.exists()) {
			throw new IllegalArgumentException("File " + stopWordsFilePath
					+ " doesn't exits.");
		}
		HashSet<String> stopWordsSet = new HashSet<String>();
		readStopWords(stopWordFile, stopWordsSet);
		return stopWordsSet;
	}
	
	/**
	 * A helper function which reads the input file and writes the words into a {@link HashSet}.
	 * @param file
	 * @param stopWordSet
	 * @throws IOException
	 */
	public static void readStopWords(File file, HashSet<String> stopWordSet)
			throws IOException {
		FileInputStream fis = null;
		BufferedReader reader = null;
		fis = new FileInputStream(file);
		String line;
		try {
			reader = new BufferedReader(new InputStreamReader(fis));
			line = reader.readLine();
			while (line != null) {
				line = line.trim().toLowerCase();
				stopWordSet.add(line);
				line = reader.readLine();
			}
		} finally {
			reader.close();
		}
		System.out.println("Read in stop words from file: "+  file.getAbsoluteFile());
	}
	
	/**
	 * Given a json input line returns a {@link JSONObject}.
	 * 
	 * @param jsonLine
	 *            A json object representing as a single line string.
	 * @return The parsed json {@link JSONObject} or null if the parse failed.
	 */
	public static JSONObject ParseJson(String jsonLine) {
		try {
			Object obj = mParser.parse(jsonLine);
			return (JSONObject) obj;
		} catch (ParseException ex) {
			System.out.println("Fail" + ex);
			ex.printStackTrace();
			return null;
		}
	}
}
