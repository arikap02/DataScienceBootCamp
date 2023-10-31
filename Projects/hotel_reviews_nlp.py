# -*- coding: utf-8 -*-
"""Hotel Reviews_NLP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zOaotIwCQl0yhJkR1HjoWAbS0XjVHsEm
"""

import pandas as pd
import numpy as np
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

df = pd.read_csv('Hotel_Reviews.csv')

df.info()

df.head()

# Create a new column in the DataFrame called 'reviewer_nation'
df['reviewer_nation'] = df['Reviewer_Nationality']

# Convert the 'reviewer_nation' column to lowerca
df['reviewer_nation'] = df['reviewer_nation'].str.lower()

# Count the number of reviewers from each nation
reviewer_nation_counts = df['reviewer_nation'].value_counts()

# Print the number of reviewers from each nation to the console
print(reviewer_nation_counts)

#a) Highest reviewers from which nationality

# Create a new column in the DataFrame called 'reviewer_nation_rating'
df['reviewer_nation_rating'] = df['Total_Number_of_Reviews_Reviewer_Has_Given']

# Group the DataFrame by 'reviewer_nation' and calculate the mean 'reviewer_rating' for each group
reviewer_nation_mean_ratings = df.groupby('Reviewer_Nationality')['Total_Number_of_Reviews_Reviewer_Has_Given'].mean()

print(reviewer_nation_mean_ratings.head(5))

def concatenate_reviews(df):

  # Create a new column to store the concatenated reviews.
  df['concatenated_reviews'] = ''

  # Iterate over the negative reviews and positive reviews columns, and concatenate
  # each pair of reviews into the new column.
  for i in range(len(df)):
    negative_review = df.loc[i, 'Negative_Review']
    positive_review = df.loc[i, 'Positive_Review']

    # If either the negative review or positive review is empty, we can
    # concatenate the other review into the new column.
    if pd.isna(negative_review):
      df.loc[i, 'concatenated_reviews'] = positive_review
    elif pd.isna(positive_review):
      df.loc[i, 'concatenated_reviews'] = negative_review
    else:
      # Concatenate the negative and positive reviews with a separator.
      df.loc[i, 'concatenated_reviews'] = f'{negative_review} || {positive_review}'

  return df

# Concatenate the negative and positive reviews together in a new column.
df = concatenate_reviews(df)

# Print the DataFrame.
print(df)

df['concatenated_reviews'].describe()

'''1) Lower Case that column
2) Remove Stop words
3) Remove punctuations
4) Apply Lemmitization/Stemming (Check accuracy with both)
5) Apply TFIDF/Count vectorizer
6) Apply model on target column Reviewer_Score
Compare results for both TF/IDF and Count vectorizer '''

# Convert the 'concatinated_reviews' column to lowercase
df['concatenated_reviews'] = df['concatenated_reviews'].str.lower()

corpus = []

# Remove the stop words
for i in range(0,1000):
  concatenated_review = re.sub('[^a-zA-Z]', ' ',  df.concatenated_reviews[i])
  ps = PorterStemmer()
  all_stopwords = stopwords.words('english')
  all_stopwords.remove('not')
  concatenated_review = [ps.stem(word) for word in concatenated_review if not word in set(all_stopwords)]
  concatenated_review = ' '.join(concatenated_review)
  corpus.append(concatenated_review)

df['concatenated_reviews']

# Apply TFIDF/Count vectorizer

from nltk.tokenize import word_tokenize
sentences = []
word_set = []

for sent in concatenated_review:
    words = [word.lower() for word in word_tokenize(sent) if word.isalpha()]
    sentences.append(words)
    for word in words:
        if word not in word_set:
            word_set.append(word)
# Set of words
word_set = set(word_set)
# total documents in our corpus
total_docs = len(concatenated_review)
print('Total documents: ', total_docs)
print('Total words: ', len(word_set))

word_index = {}
for i, word in enumerate(word_set):
    word_index[word] = i

#Calculate TF
def term_frequency(document, word):
    N = len(document)
    occurance = len([token for token in document if token == word])
    return occurance / N

# Calculate IDF
def inverse_document_frequency(word):
    try:
        word_occurance = word_count[word] + 1
    except:
        word_occurance = 1
    return np.log(total_docs / word_occurance)

#Combine TF/IDF
def tf_idf(sentence):
    vec = np.zeros((len(word_set),))
    for word in sentence:
        tf = term_frequency(sentence, word)
        idf = inverse_document_frequency(word)
        vec[word_index[word]] = tf * idf
    return vec

#Print Vectors
vectors = []
for sent in sentences:
    vectors.append(tf_idf(sent))

print(vectors)