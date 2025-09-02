import spacy


class Tokenizer:

    def __init__(self):
        self.nlp = spacy.blank("RO")

    def tokenize(self, text):
        doc = self.nlp.make_doc(text)
        return doc

if __name__ == "__main__":
    tokenizer = Tokenizer()
    text = "Care   este      adresa     centrală    a UTCN \n din Cluj-Napoca?"

    doc = tokenizer.tokenize(text)

    # Print tokens as a list
    tokens = [token.text for token in doc]
    print(tokens)