import json
import crayons

from translation import Translation
from config import Config
from typing import Any
from utils import generate_menu
from utils import cls
from utils import logo
from utils import center


class ShopGenerator:
    def __init__(self, app_name: str) -> None:
        self.app_name = app_name
        self.config = Config("config.json")
        self.translation = Translation(self.config.read().translations,self.config.read().language_map)

    def validate_item(self, item: str) -> bool:
        """
        Validates the item format.
        """
        split = item.split(":")
        valid = True
        if len(split) != 2:
            print(self.translation.get("invalid-format"))
            valid = False
        elif "_" not in split[1]:
            print(self.translation.get("invalid-format"))
            valid = False
        if not valid:
            input(self.translation.get("try-again"))
        return valid

    def build_shop(self):
        """
        Builds the shop with the user inputted items.
        """
        cls()
        config = self.config.read()
        never_end_date = "9999-12-31T23:59:59.999Z"

        base_shop: Any = {  # type:ignore
            "refreshIntervalHrs": 1,
            "dailyPurchaseHrs": 1,
            "expiration": never_end_date,
            "storefronts": [{"name": config.season, "catalogEntries": []}],
        }
        for item in self.items:

            entry: Any = {  # type:ignore
                "devName": f"[VIRTUAL]1 x pirxcy for {config.default_price} MtxCurrency",
                "offerId": None,
                "fulfillmentIds": [],
                "dailyLimit": -1,
                "weeklyLimit": -1,
                "monthlyLimit": -1,
                "categories": [],
                "prices": [
                    {
                        "currencyType": "MtxCurrency",
                        "currencySubType": "",
                        "regularPrice": config.default_price,
                        "dynamicRegularPrice": config.default_price,
                        "finalPrice": config.default_price,
                        "saleExpiration": "9999-12-31T23:59:59.999Z",
                        "basePrice": config.default_price,
                    }
                ],
                "meta": {
                    "NewDisplayAssetPath": f"/OfferCatalog/NewDisplayAssets/DAv2_{item.split(":")[1]}.DAv2_{item.split(":")[1]}",
                    "LayoutId": "VictoryVibes0603.99",
                    "TileSize": "Size_1_x_1",
                    "AnalyticOfferGroupId": "VictoryVibes0603",
                    "templateId": item,
                    "color1": config.colors.one,
                    "color2": config.colors.two,
                    "color3": config.colors.three,
                    "textBackgroundColor": config.colors.text_background,
                    "inDate": "2025-06-03T00:00:00.000Z",
                    "outDate": never_end_date,
                },
                "matchFilter": "",
                "filterWeight": 0.0,
                "appStoreId": [],
                "requirements": [
                    [
                        {
                            "requirementType": "DenyOnItemOwnership",
                            "requiredId": item,
                            "minQuantity": 1,
                        }
                    ]
                ],
                "offerType": "StaticPrice",
                "giftInfo": {
                    "bIsEnabled": True,
                    "forcedGiftBoxTemplateId": "",
                    "purchaseRequirements": [],
                    "giftRecordIds": [],
                },
                "refundable": True,
                "metaInfo": [
                    {
                        "key": "NewDisplayAssetPath",
                        "value": f"/OfferCatalog/NewDisplayAssets/DAv2_{item.split(':')[1]}.DAv2_{item.split(':')[1]}",
                    },
                    {"key": "LayoutId", "value": "VictoryVibes0603.99"},
                    {"key": "TileSize", "value": "Size_1_x_1"},
                    {"key": "AnalyticOfferGroupId", "value": "VictoryVibes0603"},
                    {"key": "templateId", "value": item},
                    {"key": "color1", "value": config.colors.one},
                    {"key": "color2", "value": config.colors.two},
                    {"key": "color3", "value": config.colors.three},
                    {
                        "key": "textBackgroundColor",
                        "value": config.colors.text_background,
                    },
                    {"key": "inDate", "value": "2025-06-03T00:00:00.000Z"},
                    {"key": "outDate", "value": never_end_date},
                ],
                "itemGrants": [{"templateId": item, "quantity": 1}],
                "additionalGrants": [],
                "sortPriority": -1,
                "catalogGroupPriority": 0,
            }
            base_shop["storefronts"][0]["catalogEntries"].append(entry)
            print(f"[+] {item.split(':')[1]}")
        return base_shop

    def store_shop(self, shop: Any) -> None:  # type:ignore
        """
        Stores the shop in the output folder.
        """
        cls()
        config = self.config.read()
        output_folder = config.output_folder

        if not output_folder.endswith("/"):
            output_folder += "/"

        with open(f"{output_folder}shop.json", "w") as file:
            json.dump(shop, file)

        print(self.translation.get("shop-generated"))
        input(self.translation.get("finish-adding"))
        self.main()

    def generate_shop_items(self):
        cls()
        items: list[str] = []

        while True:
            cls()
            print(center(logo))
            print(
                self.translation.get("stored-items").format(crayons.red(len(items)))  # type:ignore
            )  # type:ignore
            print(self.translation.get("enter-item"))
            print(self.translation.get("enter-item-format"))  # type:ignore
            print(self.translation.get("finish-adding"))
            item = input(self.translation.get("item"))

            if item == "":
                break

            if self.validate_item(item):
                items.append(item)

        self.items = items
        shop = self.build_shop()
        self.store_shop(shop)

        return

    def main(self):
        options: dict[str, Any] = {
            self.translation.get("generate-shop"): self.generate_shop_items,
            self.translation.get("exit"): exit,
        }
        option = generate_menu(options=options, text=self.translation.get("welcome"))
        option()

    def run(self):
        self.main()


if __name__ == "__main__":
    app = ShopGenerator("pirxcy's Fortnite Shop Generator")
    app.run()
