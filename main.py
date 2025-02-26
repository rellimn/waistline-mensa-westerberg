from datetime import datetime
from urllib.parse import urljoin
from urllib.request import urlopen

from pydantic import BaseModel, Field, AnyUrl

img_url_base = "https://swosy.rocket-meals.de/rocket-meals/api/assets/"
food_offers_url = 'https://swosy.rocket-meals.de/rocket-meals/api/items/foodoffers?limit=-1&filter={"canteen":"fd99cdef-bb1d-4422-a48f-41310f652b3f","date":{"_gt":"today"}}&fields=*,food.image'


class Img(BaseModel):
    image: str | None = None


class Nutrition(BaseModel):
    calories: float | None = Field(validation_alias="calories_kcal", default=None)
    carbohydrates: float | None = Field(validation_alias="carbohydrate_g", default=None)
    sugars: float | None = Field(validation_alias="sugar_g", default=None)
    fat: float | None = Field(validation_alias="fat_g", default=None)
    saturated_fat: float | None = Field(serialization_alias="saturated-fat", validation_alias="saturated_fat_g",
                                        default=None)
    proteins: float | None = Field(validation_alias="protein_g", default=None)
    salt: float | None = Field(validation_alias="salt_g", default=None)


class InData(Nutrition):
    alias: str
    image: Img = Field(alias="food")
    date: datetime


class In(BaseModel):
    data: list[InData]


class OutFood(BaseModel):
    name: str
    image_url: AnyUrl | None
    brand: str = "Mensa Westerberg"
    uniqueId: str
    portion: float = 1.0
    unit: str = "meal"
    nutrition: Nutrition


class Out(BaseModel):
    version: int = 1
    foodList: list[OutFood]

print("Downloading food offers...")
with urlopen(food_offers_url) as f:
    in_model = In.model_validate_json(f.read())

visited_foods = {}  # map food.alias to food
for food in in_model.data:
    if food.calories and (food.alias not in visited_foods or food.date > visited_foods.get(food.alias).date):
        visited_foods[food.alias] = food

out_foods = [
    OutFood(name=food.alias, uniqueId=str(hash(food.alias)), nutrition=food,
            image_url=urljoin(img_url_base, food.image.image) if food.image.image else None)
    for food in visited_foods.values()
]

print("Saving import.json...")
with open("import.json", "w", encoding="UTF-8") as f:
    f.write(Out(foodList=out_foods).model_dump_json(indent=2, by_alias=True))
