from json import load
from pydantic import BaseModel


class ConfigColorModel(BaseModel):
    one: str
    two: str
    three: str
    text_background: str


class ConfigModel(BaseModel):
    season: str
    default_price: int
    colors: ConfigColorModel
    output_folder: str
    use_translations: bool
    language_map: dict[str, str]
    translations: dict[str, dict[str, str]]


class Config:
    def __init__(self, path: str):
        self.path = path

    def read(self) -> ConfigModel:
        with open(self.path,encoding="utf-8") as file:
            data = load(file)

        model = ConfigModel.model_validate(data)
        return model
