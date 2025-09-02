import re

class Normalizer:
    def normalize(self, text):
        print(text)
        changed_text = text.lower()
        changed_text = re.sub(r'[^a-zA-Z0-9ăĂâÂîÎșȘțȚ,.\-_\s]', '', changed_text)
        changed_text = changed_text.replace('\n', ' ').replace('\t', ' ')
        changed_text = ' '.join(changed_text.split())
        print(changed_text)
        return changed_text

if __name__ == "__main__":
    normalizer = Normalizer()
    sample_text = "cĂmin   salut"
    normalized_text = normalizer.normalize(sample_text)
    print("Original:", sample_text)
    print("Normalized:", normalized_text)