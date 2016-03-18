Run PageRank on Urban Dictionary
Brian Xie, Emily Miller, Quinn Tran
Main Idea:
Run Pagerank on a root (word) to find the most popular words synonymous to the root word’s definition. Extension: Find out which words are trending since it is entirely users contribute to the relationship links between words.
Urbandictionary creates a page for each word entry, which may have multiple definitions for a given word. These pages are connected to one another in three ways:
-Each word’s page contains references to the pages of “related” words (determined by Urbandictionary’s internal algorithms)
-Users, in their entries for words, may also include references to pages of other words used in their definitions
-Every page has a reference to a “random word” button, so the implementation can be adjusted so that there are no dead ends/isolated nodes.

We will be exploring entire set of words with entries  on Urbandictionary. We will select an initial word, and from each word travel to one of the words referenced in a definition or the related words section; for words with no outgoing links, we will select a new random word.
We expect our results to provide new information about the words that occur with the highest frequency in the lexicons of Urbandictionary users. Urbandictionary does contain a list of popular words, but these may be sorted by some other metric, such as upvotes or staff picks; this may list words that are considered interesting, but not words which are actually used. In addition, because our Pagerank links to related words as well, we can gather a higher-level overview of the topics which users are concerned with.

PseudoCode:
d = max depth to explore each root word
root_words = {most popular words in A,B,...Z}
universal_counter = {word : # appearances = 1}
associated_words = {root_word : associates}
for each root_word:
	counter = {word: # appearances = 0}
	words_related = {links to related words}
	for each word in words_related with depth <= d:
		universal_counter[word] += 1
		associated_words[root_word].append(word)
		if word is a terminal state:
			root_words += random_word
		else:
			counter[word] += 1
			visit(word) and update counter
for each root_word:
	return most frequent related words
