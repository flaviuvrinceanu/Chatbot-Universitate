from .utils.exceptions.Exceptions import BannedWordException


class Filter:
 def filter_banned_words_foreign(self, tokens, initials):
     import json
     f = 'Preprocessor/JSON/banned_words/build.json'
     with open(f, 'r', encoding='utf-8') as file:
         banned_words = json.load(file)
     for token in tokens:
         if token in banned_words[initials]:
             raise BannedWordException
     return 0

 def filter_banned_words_english(self, tokens):
     import json
     f = 'Preprocessor/JSON/banned_words/_en.json'
     with open(f, 'r', encoding='utf-8') as file:
         banned_words = json.load(file)
     for token in tokens:
         if token in banned_words:
             raise BannedWordException
     return 0

 def filter(self, tokens):
     self.filter_banned_words_foreign(tokens, 'ro')
     self.filter_banned_words_english(tokens)

