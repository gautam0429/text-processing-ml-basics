import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK resources
nltk.download("punkt")
nltk.download("stopwords")

text = "The course was GREAT, but the video was lagging!! I am doing great in my life and i want to be movie explainer and want to be content creator along with business man i am not figuring out what i have to do in life but right now i am focussing on to get a job as a fresher "

# 1. Convert text to lowercase
text = text.lower()

# 2. Remove punctuation
text = text.translate(str.maketrans("", "", string.punctuation))

# 3. Tokenize the text
tokens = word_tokenize(text)

# 4. Remove common stop words
stop_words = set(stopwords.words("english"))
cleaned_tokens = [
    word for word in tokens if word not in stop_words
]

print("Cleaned text:", cleaned_tokens)