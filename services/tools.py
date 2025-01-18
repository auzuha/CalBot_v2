from langchain_core.tools import tool

from models.models import Food, FoodBase, Macros, Micros, Micronutrient, FoodItem

from services.database import session
from models.schemas import Food as FoodTable, FoodLogs as FoodLogsTable, Macro as MacroTable

from langchain_openai import ChatOpenAI

from services.utils import start_of_today_in_ist

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI()

@tool
def get_food_info(food: FoodBase) -> Food:
    """
    Get information for a specific food item. Use only when user specifically asks for information.
    """
    name = food.name
    exists = session.query(FoodTable, MacroTable).join(FoodTable).filter_by(name=name).first()
    if not exists:
        return f"No information found on {name}."
    query_result = session.query(FoodTable, MacroTable).join(FoodTable).filter_by(name=name)
    for food, macro in query_result:
        print(food.name, macro.calories)
        information = {'name': food.name, 'calories' : macro.calories, 'carbs': macro.carbs, 'protein': macro.protein, 'fat': macro.fat, 'fiber': macro.fiber} ###
    return information
    
@tool
def add_new_food_to_database(food: Food):
    """
    Add information about a new food item to the database. If anything is missing, ask for it, don't make it up.
    """
    
    print('in add food item')
    food_dict = food.dict()
    print(food_dict)
    unset_attributes = [key for key,value in food_dict['macros'].items() if value == -1]
    print(unset_attributes)
    if not unset_attributes:
        food = FoodTable(name=food_dict['name'])
        macros = food_dict['macros']
        macro = MacroTable(calories=macros['calories'], carbs=macros['carbs'], protein=macros['protein'], fat=macros['fat'], fiber=macros['fiber'], food=food)
        if macros.get('serving_size'):
            macro.serving_size = macros['serving_size']
        session.add_all([food, macro])
        session.commit()
        return "Food item successfully added into the database."
    tool_response = f'Still need the following: {",".join(unset_attributes)}'
    return tool_response
    
@tool
def add_food_to_daily_log(fooditem: FoodItem):
    """
    Add a food item to the daily log.
    """
    food = session.query(FoodTable).filter_by(name=fooditem.name).first()
    food_item = FoodLogsTable(name=fooditem.name, quantity=fooditem.quantity, unit=fooditem.unit,food=food)
    session.add_all([food_item])
    session.commit()
    return "Food item successfully logged."

@tool
def get_daily_log():
    """
    Get the daily log of the food user has eaten
    """
    foods_logged_today = session.query(FoodLogsTable).filter(FoodLogsTable.created_at >= start_of_today_in_ist())
    foods_logged_today_macros = []
    total_macros_for_today = {'calories': 0, 'carbs': 0, 'protein': 0, 'fat': 0, 'fiber': 0}
    for food in foods_logged_today:
        macros_for_food = session.query(MacroTable).filter_by(food_id=food.food_id).first()
        if food.unit == 'N':
            multiplier = food.quantity * macros_for_food.serving_size / 100
        else:
            multiplier = food.quantity / 100
        adjusted_macros = {'name': food.name,'quantity': f'{food.quantity}{food.unit}','calories': multiplier*macros_for_food.calories, 'carbs': multiplier*macros_for_food.carbs,'protein': multiplier*macros_for_food.protein,'fat': multiplier*macros_for_food.fat,'fiber': multiplier*macros_for_food.fiber}
        for key, value in total_macros_for_today.items():
            total_macros_for_today[key] += adjusted_macros[key]
        foods_logged_today_macros.append(adjusted_macros)
    print(foods_logged_today_macros)
    return f"Below is your daily log of food items eaten:\n{foods_logged_today_macros}\n\nTotal Macros:{total_macros_for_today}"
