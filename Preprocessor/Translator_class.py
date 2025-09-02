class Translator:
    def intent_to_request(self, intent):
        import json
        f = 'Preprocessor/JSON/intent_dictionary.json'
        with open(f, 'r', encoding='utf-8') as file:
            request = json.load(file)
        try:
            return request[intent][0]
        except KeyError:
            return "No valid response found!"

if __name__ == "__main__":
    translator = Translator()
    intent = "portal_login"
    print(translator.intent_to_request(intent))