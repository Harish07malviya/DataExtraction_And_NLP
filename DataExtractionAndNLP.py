import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import openpyxl
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import cmudict
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import syllapy
import re


# Download 
nltk.download('cmudict')

# Initialize NLTK Vader Sentiment Analyzer
nltk.download('vader_lexicon')


# Code For Data Extraction 
# # Output folder name
# output_folder = 'urls_article'

# if not os.path.exists(output_folder):
#     # Create folder if it not exists
    
#     os.makedirs(output_folder, exist_ok=True)
# else:
#     print(f"This folder {output_folder} is alredy exists.")


# # Read the input.xlsx file
# df = pd.read_excel('input.xlsx')

# # Display the URL_ID and URL using loop 
# for index in df.index:
#     url_id = df.at[index, 'URL_ID']
#     url = df.at[index, 'URL']
#     print(f"{url_id},     {url}")
    
    
# # Fetch HTML content from the url's
#     r = requests.get(url)


#     headers = ({
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
#      'Accept-Language': 'eg-US,en;q=0.5' }) 
# # Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link. 
#     r = requests.get(url, headers=headers)


#     if r.status_code == 200:
#         htmlContent = r.text
    
#     # parsing
#         soup = BeautifulSoup(htmlContent, 'html.parser')

    
# # Extract Article Title 
#         articleTitle = soup.title.get_text() if soup.title else "Untitled"


# # Extract article content
#         articleText = articleTitle + '\n\n' 
#         for tag in soup.find_all(['h2', 'p']):
#             if tag.name == 'h2':
#         # Include <h2> tag text as headings
#                 articleText += f"\n\n{tag.get_text(strip=True)}\n"
#             elif tag.name == 'p' and not tag.find_parents(['header', 'footer']):
#         # Include <p> tag text, excluding header and footer paragraphs
#                 articleText += f"{tag.get_text(strip=True)}\n"
    
    
# # Save the Extracted Article Content with their URL_ID as its file name   
#         file_path = os.path.join(output_folder, f"{url_id}.txt")
#         with open(file_path, "w", encoding="utf-8") as text_file:
#             text_file.write(articleText)
#     else:
#         print(f"Failed to fetch {url}")
    
# print("Extraction and saving the urls article complete")


# Stop Words File's Text
stopWords = set()
# File Path
StopWordsPath = 'StopWords'
# Combine all text
CombineStopWords = []
for filename in os.listdir(StopWordsPath):
    file_path = os.path.join(StopWordsPath, filename)
    with open(file_path, 'r') as f:
        stopWords = [line.strip().lower() for line in f]
        CombineStopWords.extend(stopWords)
        
# Cleaning the Article's Data Using Stop Words list       
urls_data = {}
urls_article_dir = 'urls_article'  # Replace with your directory path

# Read and clean text files
for filename in os.listdir(urls_article_dir):
  filepath = os.path.join(urls_article_dir, filename)
  if os.path.isfile(filepath):
    try:
      with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        filtered_words = [word for word in content.split() if word.lower() not in stopWords]
        cleaned_text = " ".join(filtered_words)
        urls_data[filename] = cleaned_text
        # print(f"Read and cleaned {filename}")

      # Save the cleaned text to the original filename
      output_filepath = os.path.join(urls_article_dir, filename)  # Same directory for output
      with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
        # print(f"Saved cleaned text to {filename}")
        
    except UnicodeDecodeError:
      print(f"Warning: Couldn't decode {filepath}. Skipping.")
      

# Master Dictionary File's 
PositiveMasterDictionary = []
NegativeMasterDictionary = []

# Positive MasterDictionary File Path
PositiveMasterDictionaryPath = 'MasterDictionary/Positive-words.txt'
# Negative MasterDictionary File Path
NegativeMasterDictionaryPath = 'MasterDictionary/Negative-words.txt'

# Positive Words
with open(PositiveMasterDictionaryPath, 'r') as f:
    Positive = [line.strip().lower() for line in f]
    PositiveMasterDictionary = Positive
    
# Negative Words
with open(NegativeMasterDictionaryPath, 'r') as f:
    Negative = [line.strip().lower() for line in f]
    NegativeMasterDictionary = Negative
    
    
# Initialize CMU Pronouncing Dictionary
cmu_dict = cmudict.dict()

# Initialize NLTK Vader Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Initialize regex pattern for personal pronouns
personal_pronoun_pattern = re.compile(r'\b(?:I|we|my|ours|us)\b', flags=re.IGNORECASE)

# Initialize output data list
output_data = []

# Load input Excel file
input_file = "input.xlsx"
input_data = pd.read_excel(input_file)

# Load content from text files in urls_article directory
urls_data = {}
urls_article_dir = 'urls_article'
for filename in os.listdir(urls_article_dir):
    filepath = os.path.join(urls_article_dir, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            urls_data[filename] = f.read()

# Process each row in input data
for index, row in input_data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
for url_id, content in urls_data.items():
    # Tokenize the text
    tokens = word_tokenize(content.lower())

    # Remove stop words and punctuation
    clean_tokens = [token for token in tokens if token not in stopWords and token.isalnum()]

    # Count total words after cleaning
    total_words = len(clean_tokens)

    # Tokenize the content into sentences
    sentences = sent_tokenize(content)

    # Count total sentences
    total_sentences = len(sentences)

    # Calculate positive and negative scores
    positive_score = sum(1 for token in clean_tokens if token in PositiveMasterDictionary)
    negative_score = sum(1 for token in clean_tokens if token in NegativeMasterDictionary)

    # Adjust negative score to make it positive
    negative_score *= -1
    
    # Calculate Polarity Score
    polarity_score = (positive_score - negative_score) / (positive_score + negative_score + 0.000001)
    polarity_score = round(polarity_score, 3)  # Rounding to three decimal places

    # Calculate Subjectivity Score
    subjectivity_score = (positive_score + negative_score) / (total_words + 0.000001)
    subjectivity_score = round(subjectivity_score, 3)  # Rounding to three decimal places

    # Calculate average number of words per sentence
    avg_words_per_sentence = total_words / total_sentences

    # Calculate percentage of complex words
    complex_words_count = sum(1 for word in clean_tokens if word.lower() in cmu_dict and max(len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[word.lower()]) > 2)
    percentage_complex_words = complex_words_count / total_words

    # Calculate Fog Index
    fog_index = 0.4 * (avg_words_per_sentence + percentage_complex_words)

    # Calculate personal pronouns count
    personal_pronouns_count = len(re.findall(personal_pronoun_pattern, content))

    # Calculate average word length
    average_word_length = sum(len(word) for word in clean_tokens) / total_words
    
    # Calculate syllables per word using syllapy
    syllable_per_word = sum(syllapy.count(word) for word in clean_tokens) / total_words
        

    # Append the calculated metrics to the output data
    output_data.append({
        'URL_ID': url_id,
        'URL': url,
        'Positive Score': positive_score,
        'Negative Score': negative_score,
        'Polarity Score': polarity_score,
        'Subjectivity Score': subjectivity_score,
        'Avg Sentence Length': avg_words_per_sentence,
        'Percentage of Complex Words': percentage_complex_words,
        'Fog Index': fog_index,
        'Avg Number of Words Per Sentence': avg_words_per_sentence,
        'Complex Word Count': complex_words_count,
        'Word Count': total_words,
        'Syllable Per Word': syllable_per_word,
        'Personal Pronouns': personal_pronouns_count,
        'Avg Word Length': average_word_length
    })

# Create a DataFrame from the output data
output_df = pd.DataFrame(output_data)

# Save DataFrame to CSV file
output_csv_file = "output_data_structure.csv"
output_df.to_csv(output_csv_file, index=False)

print("Output data saved to:", output_csv_file)
