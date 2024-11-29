import re
from collections import Counter

def analyze_text(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        words = re.findall(r'\b\w+\b', text.lower())
        sentences = re.split(r'[.!?]', text)
        word_count = len(words)
        sentence_count = len([s for s in sentences if s.strip()])
        most_common = Counter(words).most_common(5)
        
        print(f"Word count: {word_count}")
        print(f"Sentence count: {sentence_count}")
        print(f"Most common words: {most_common}")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")

if __name__ == "__main__":
    file_path = input("Enter the path to your text file: ")
    analyze_text(file_path)