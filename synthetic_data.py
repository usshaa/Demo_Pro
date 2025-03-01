import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Set random seed for reproducibility
np.random.seed(42)

# Generate user data
user_count = 500
role_types = ['Software Developer', 'Data Scientist', 'DevOps Engineer', 
              'Network Administrator', 'Security Analyst', 'UX Designer', 
              'Product Manager', 'Database Administrator', 'Cloud Architect', 
              'AI Engineer']

users = []
for i in range(1, user_count + 1):
    role = np.random.choice(role_types)
    experience = np.random.choice(['Entry Level', 'Mid Level', 'Senior'])
    users.append({
        'user_id': i,
        'role': role,
        'experience_level': experience
    })

users_df = pd.DataFrame(users)

# Generate course data
course_count = 200
course_types = ['Programming', 'Data Science', 'Cloud Computing', 'Security', 
                'Networking', 'DevOps', 'Design', 'Databases', 'Product Management',
                'AI & Machine Learning', 'Web Development', 'Mobile Development']

courses = []
for i in range(1, course_count + 1):
    course_type = np.random.choice(course_types)
    difficulty = np.random.choice(['Beginner', 'Intermediate', 'Advanced'])
    duration = np.random.randint(1, 20) * 5  # Course duration in hours
    courses.append({
        'course_id': i,
        'title': f"{course_type} Course {i}",
        'type': course_type,
        'difficulty': difficulty,
        'duration_hours': duration,
        'avg_rating': round(np.random.uniform(3.0, 5.0), 1)
    })

courses_df = pd.DataFrame(courses)

# Generate ratings
ratings = []
# Each user rates 5-20 courses
for user_id in users_df['user_id']:
    # Select random courses for this user to rate
    num_ratings = np.random.randint(5, 21)
    rated_courses = np.random.choice(courses_df['course_id'], size=num_ratings, replace=False)
    
    for course_id in rated_courses:
        # Generate rating based on user role and course type to create realistic patterns
        user_role = users_df.loc[users_df['user_id'] == user_id, 'role'].iloc[0]
        course_type = courses_df.loc[courses_df['course_id'] == course_id, 'type'].iloc[0]
        
        # Add some role-course affinity
        affinity = 0
        if (user_role == 'Software Developer' and course_type in ['Programming', 'Web Development']):
            affinity = 1
        elif (user_role == 'Data Scientist' and course_type in ['Data Science', 'AI & Machine Learning']):
            affinity = 1
        elif (user_role == 'DevOps Engineer' and course_type in ['DevOps', 'Cloud Computing']):
            affinity = 1
        # Add more role-course type affinities...
        
        # Generate rating with some noise and affinity bias
        base_rating = np.random.normal(3.5, 0.8)
        rating = min(5, max(1, base_rating + affinity + np.random.normal(0, 0.5)))
        
        ratings.append({
            'user_id': user_id,
            'course_id': course_id,
            'rating': round(rating, 1)
        })

ratings_df = pd.DataFrame(ratings)

# Save the synthetic data
users_df.to_csv('users.csv', index=False)
courses_df.to_csv('courses.csv', index=False)
ratings_df.to_csv('ratings.csv', index=False)

print(f"Generated {len(users_df)} users, {len(courses_df)} courses, and {len(ratings_df)} ratings")