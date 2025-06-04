import locale

class Translation:
    def __init__(self, translations: dict[str, dict[str, str]],map:dict[str, str]) -> None:
        self.translations = translations
        self.language = map.get((locale.getdefaultlocale()[0] or "en").split("_")[0], "english")


    def get(self, text: str) -> str:
        return self.translations[text][self.language]
