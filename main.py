import gradio as gr

from services.graph import get_bot_response

from services import config

from models.schemas import Food, Macro
from services.database import session

def add_food_item(food_name, calories, carbs, protein, fat, fiber, serving_size):
    # Validation to check if food is in the database.
    if not food_name or not isinstance(food_name, str):
        return "Food name must be a non-empty string."
    try:
        # Convert inputs to the correct types (int or float)
        calories = float(calories)
        carbs = float(carbs)
        protein = float(protein)
        fat = float(fat)
        fiber = float(fiber)
        serving_size = float(serving_size)
    except ValueError:
        return "All numeric fields (calories, carbs, protein, fat, fiber, and serving size) must be valid numbers."

    if any(val < 0 for val in [calories, carbs, protein, fat, fiber, serving_size]):
        return "All numeric values must be greater than or equal to zero."

    # Print the collected data
    food_data = {
        "Food Name": food_name,
        "Calories": calories,
        "Carbs (g)": carbs,
        "Protein (g)": protein,
        "Fat (g)": fat,
        "Fiber (g)": fiber,
        "Serving Size": serving_size
    }
    food = Food(name=food_name) 
    macro = Macro(calories=calories, carbs=carbs, protein=protein, fat=fat,fiber=fiber, food=food)
    session.add_all([food,macro])
    session.commit()
    print(food_data)  # Print the data to the console
    return f"Food item added:\n{food_data}"



def chat_interface(message, history):
    response = get_bot_response(message, history)
    history.append((message, response))
    return "", history

# Define the Gradio interface for the chat
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            chat_history = gr.Chatbot()
            message = gr.Textbox(label="Your message")
            send_button = gr.Button("Send")

            # Add the new food item section
            food_name = gr.Textbox(label="Food Name")
            calories = gr.Number(label="Calories", value=0)
            carbs = gr.Number(label="Carbs (g)", value=0)
            protein = gr.Number(label="Protein (g)", value=0)
            fat = gr.Number(label="Fat (g)", value=0)
            fiber = gr.Number(label="Fiber (g)", value=0)
            serving_size = gr.Textbox(label="Serving Size")
            add_food_button = gr.Button("Add New Food Item")
            food_output = gr.Textbox(label="Food Item Info", interactive=False)

    # Define actions for the buttons
    send_button.click(chat_interface, inputs=[message, chat_history], outputs=[message, chat_history])
    add_food_button.click(add_food_item, inputs=[food_name, calories, carbs, protein, fat, fiber, serving_size], outputs=food_output)

# Launch the interface




def main():
    demo.launch()    

main()