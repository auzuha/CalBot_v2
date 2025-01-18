from pydantic.v1 import BaseModel, Field
from typing import List, Union, Optional

## pydantic schemas

class Macros(BaseModel):
    calories: int = Field(description="The amount of calories in the food item per serving. -1 if unspecified.")
    protein: float = Field(description="The amount of protein in the food item per serving. -1 if unspecified.")
    carbs: float = Field(description="The amount of carbohydrates in the food item per serving. -1 if unspecified.")
    fat: float = Field(description="The amount of fat in the food item per serving. -1 if unspecified.")
    fiber: float = Field(description="The amount of fiber in the food item per serving. -1 if unspecified.")

class Micronutrient(BaseModel):
    attr_id: Union[str, int] = Field(description="The usda attribue id of the micronutrient.")
    name: str = Field(description="The name of the micro nutrient")
    value: float = Field(default=0, description="The amount of the micronutrient in the food item (in mg).")


class Micros(BaseModel):
    micros: List[Micronutrient]

class FoodBase(BaseModel):
    name: str = Field(default="", description="Name of the food item. Always in lowercase, and snake_case")

class Food(FoodBase):
    serving_size: int = Field(default=100, description="Serving size of one portion (in grams).")
    macros: Macros

class FoodItem(FoodBase):
    #name: str = Field(default="", description="Name of the food item.")
    quantity: float = Field(description="The quantity of the food item to be logged. -1 if unspecified.")
    unit: str = Field(description="The unit of the amount, either in grams [gm], or the quantity, [N].")

