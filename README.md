# DataExtraction-And-NLP

# 1. Approach to the Solution:

## Data Extraction:

Read URLs from the provided Input.xlsx file.
Utilize the Python library BeautifulSoup to extract article text from each URL, focusing on the title and main content while ignoring headers, footers, and other irrelevant sections.
Save the extracted article text in separate text files, naming them with the respective URL_ID.
## Data Analysis:

Read the extracted article text from the text files.
Perform text analysis using NLTK or other natural language processing libraries to compute the required variables such as positive score, negative score, polarity score, etc., as per the definitions provided in the "Text Analysis.docx" document.
Organize the computed variables according to the provided output structure and save them to an Excel file.


# 2. Running the .py file to Generate Output:

## Steps:

Ensure you have Python installed on your system.
Install the necessary dependencies by running pip install pandas nltk syllapy in your terminal or command prompt.
Download and place the cmudict corpus in the NLTK data directory (if using NLTK for syllable count).
Place the Input.xlsx file in the same directory as your Python script.
Run the Python script (data_extraction_and_nlp.py or any other name you choose) using a Python interpreter.


# 3. Dependencies Required:

## Python Libraries:

pandas: For data manipulation and handling Excel files.
nltk (Natural Language Toolkit): For text analysis tasks like tokenization, sentiment analysis, etc.
syllapy: For counting syllables in words.
Ensure you have these libraries installed in your Python environment. If not, you can install them using pip install followed by the library name.
