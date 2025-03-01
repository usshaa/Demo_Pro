# app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
from surprise import Reader

app = Flask(__name__)

# Load the data and model
users_df = pd.read_csv('users.csv')
courses_df = pd.read_csv('courses.csv')
ratings_df = pd.read_csv('ratings.csv')
model = joblib.load('course_recommender_model.pkl')

@app.route('/')
def home():
    roles = sorted(users_df['role'].unique())
    experience_levels = sorted(users_df['experience_level'].unique())
    return render_template('index.html', roles=roles, experience_levels=experience_levels)

@app.route('/recommend', methods=['POST'])
def recommend():
    user_id = request.form.get('user_id')
    role = request.form.get('role')
    experience = request.form.get('experience')
    
    # If user_id is provided, use it for recommendations
    if user_id and user_id.isdigit() and int(user_id) in users_df['user_id'].values:
        user_id = int(user_id)
        recommendations = get_recommendations_for_user(user_id)
    # Otherwise, create a new user profile based on role and experience
    else:
        recommendations = get_recommendations_for_new_user(role, experience)
    
    return jsonify(recommendations)

def get_recommendations_for_user(user_id):
    # Get all courses the user hasn't rated yet
    rated_courses = ratings_df[ratings_df['user_id'] == user_id]['course_id'].tolist()
    courses_to_predict = [c for c in courses_df['course_id'] if c not in rated_courses]
    
    # Predict ratings for all unrated courses
    predictions = []
    for course_id in courses_to_predict:
        pred = model.predict(user_id, course_id)
        predictions.append((course_id, pred.est))
    
    # Sort by predicted rating
    predictions.sort(key=lambda x: x[1], reverse=True)
    top_10_course_ids = [p[0] for p in predictions[:10]]
    
    # Get course details
    recommended_courses = courses_df[courses_df['course_id'].isin(top_10_course_ids)].copy()
    
    # Add predicted ratings
    for i, row in recommended_courses.iterrows():
        course_id = row['course_id']
        predicted_rating = next(p[1] for p in predictions if p[0] == course_id)
        recommended_courses.at[i, 'predicted_rating'] = round(predicted_rating, 1)
    
    # Sort by predicted rating
    recommended_courses = recommended_courses.sort_values('predicted_rating', ascending=False)
    
    return recommended_courses.to_dict('records')

def get_recommendations_for_new_user(role, experience):
    # Get average ratings for each course by role
    role_course_ratings = pd.merge(ratings_df, users_df, on='user_id')
    role_course_ratings = pd.merge(role_course_ratings, courses_df, on='course_id')
    
    # Filter by role if provided
    if role:
        role_filtered = role_course_ratings[role_course_ratings['role'] == role]
        if len(role_filtered) > 0:
            role_course_ratings = role_filtered
    
    # Get average ratings for each course
    avg_ratings = role_course_ratings.groupby('course_id')['rating'].mean().reset_index()
    
    # Join with course information
    course_ratings = pd.merge(avg_ratings, courses_df, on='course_id')
    
    # Adjust for experience level if provided
    if experience:
        if experience == 'Entry Level':
            course_ratings = course_ratings[course_ratings['difficulty'] == 'Beginner']
        elif experience == 'Mid Level':
            course_ratings = course_ratings[course_ratings['difficulty'].isin(['Beginner', 'Intermediate'])]
    
    # Get top 10 courses
    top_courses = course_ratings.sort_values('rating', ascending=False).head(10)
    top_courses = top_courses.rename(columns={'rating': 'predicted_rating'})
    
    return top_courses.to_dict('records')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)