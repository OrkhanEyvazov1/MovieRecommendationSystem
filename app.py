# app.py

import gradio as gr
import pickle
import numpy as np
import pandas as pd

# Load the trained CatBoost model
try:
    with open('catboost_model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    # This is a fallback for testing if the model isn't present.
    # The real deployment will fail if the model is missing.
    print("Error: `catboost_model.pkl` not found. The app will not work correctly.")
    model = None

# Define the list of all possible genres from your training script
ALL_GENRES = [
    'Adventure', 'Comedy', 'Action', 'Mystery', 'Crime', 'Thriller',
    'Drama', 'Animation', 'Children', 'Horror', 'Documentary',
    'Sci-Fi', 'Fantasy', 'Film-Noir', 'Western', 'Musical', 'Romance',
    '(no genres listed)', 'War'
]

def predict_rating(movie_year, selected_genres, user_views, user_avg_rating):
    """
    Takes user input from the Gradio interface, transforms it into the format
    expected by the model, and returns a prediction.
    """
    if model is None:
        return "Model not loaded. Cannot make a prediction."

    # 1. Start with the movie year.
    feature_list = [movie_year]

    # 2. Create the one-hot encoded genre features.
    # The model expects a 0 or 1 for each genre in the specific order.
    for genre in ALL_GENRES:
        if genre in selected_genres:
            feature_list.append(1)
        else:
            feature_list.append(0)

    # 3. Add the user-specific features.
    feature_list.append(user_views)
    feature_list.append(user_avg_rating)

    # Convert the list into the format required by the model for prediction
    # (e.g., a numpy array or a pandas DataFrame).
    # Based on your training script, a DataFrame with correct column names is safest.
    
    # Define column names based on your training script's X_train
    column_names = ['movieYear'] + ALL_GENRES + ['userViews', 'userMeans']
    
    # Create a DataFrame for the single prediction
    user_data_df = pd.DataFrame([feature_list], columns=column_names)

    # 4. Make the prediction.
    prediction = model.predict(user_data_df)

    # Return the predicted rating, formatted to 2 decimal places.
    return f"Predicted Rating: {prediction[0]:.2f}"

# Create the Gradio Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎬 Movie Rating Predictor")
    gr.Markdown("Enter the movie details and user history to predict the movie's rating.")
    
    with gr.Row():
        with gr.Column():
            movie_year_input = gr.Number(label="Movie Release Year", value=2005, step=1)
            user_views_input = gr.Number(label="How many movies has this user watched?", value=150)
            user_avg_rating_input = gr.Slider(minimum=0.5, maximum=5.0, step=0.1, label="What is the user's average rating?", value=3.5)
            genre_input = gr.CheckboxGroup(choices=ALL_GENRES, label="Select Movie Genres")
        
        with gr.Column():
            output_text = gr.Textbox(label="Prediction Result")

    predict_btn = gr.Button("Predict Rating")
    predict_btn.click(
        fn=predict_rating,
        inputs=[movie_year_input, genre_input, user_views_input, user_avg_rating_input],
        outputs=output_text
    )

# Launch the app. server_name="0.0.0.0" is crucial for Docker.
demo.launch(server_name="0.0.0.0", server_port=7860)