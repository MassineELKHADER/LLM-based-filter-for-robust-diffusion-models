import re

def remove_newlines(text):
        return text.replace('\n', '')

def remove_urls(text):
    url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.sub(url_regex, '', text)

def remove_html_tags(text):
    html_regex = r'<[^>]+>'
    return re.sub(html_regex, '', text)

def remove_special_characters(text):
    special_chars_regex = r'[^a-zA-Z0-9\s]'  
    return re.sub(special_chars_regex, '', text)

def remove_numbers(text):
    return re.sub(r'\d+', '', text)

def remove_extra_spaces(text):
    return re.sub(r'\s+', ' ', text)

def remove_twitter_mentions(text):
    return re.sub(r'@([A-Za-z0-9_]+)', '', text)

def remove_emoticons(text):
    emoticon_regex = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251\U0001F004\U0001F0CF\U0001F170-\U0001F251\U0001F600-\U0001F64F\U00002702-\U000027B0\U000024C2-\U0001F251\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F773\U0001F780-\U0001F7D8\U0001F7E0-\U0001F7EB\U0001F7F0-\U0001F7FF\U0001F800-\U0001F80B\U0001F90D-\U0001F9FF\U0001FA70-\U0001FA74\U0001F600-\U0001F64F\U0001F90D-\U0001F971\U0001F973-\U0001F978\U0001F97A-\U0001F9CB\U0001F9CD-\U0001F9FF]+'
    return re.sub(emoticon_regex, '', text)

def normalize_case(text):
    return text.lower()

def remove_unnecessary_spaces(text):
    text = text.strip()  
    text = re.sub(r'\s+', ' ', text)
    return text

def remove_punctuation_and_brackets(text):
    text = re.sub(r'[^\w\s\[\]]', '', text)
    return text

def remove_numbered_brackets(text):
    text = re.sub(r'\[\d+\]', '', text)
    return text
def remove_initial_article(text):
    words_to_remove = [
    'a', 'an', 'the', 'some', 'many', 'much', 'few', 'little', 
    'several', 'a few', 'a little', 'a lot of', 'lots of', 'plenty of', 
    'this', 'that', 'these', 'those', 'its' ]
    words = text.split()
    if words and words[0].lower() in words_to_remove:
        words.pop(0)
    return ' '.join(words)

def remove_initial_article(text):
    words_to_remove = ['a', 'an', 'the', 'some', 'this', 'that', 'these', 'those', 'it', 'is', 'was', 'were', 'are', 'there', 'here']
    words = text.split()
    if words and words[0].lower() in words_to_remove:
        words.pop(0)
    return ' '.join(words)  
    
def preprocess_text(text):
    text = remove_newlines(text)
    text = remove_punctuation_and_brackets(text)
    text = remove_special_characters(text)
    text = remove_urls(text)
    text = remove_html_tags(text)
    text = remove_numbers(text)
    text = remove_extra_spaces(text)
    text = remove_twitter_mentions(text)
    text = remove_emoticons(text)
    text = normalize_case(text)
    text = remove_unnecessary_spaces(text)
    text = remove_numbered_brackets(text)
    text=remove_initial_article(text)
    return text


