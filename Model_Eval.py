from surprise import accuracy
from surprise.model_selection import train_test_split as surprise_train_test_split
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from surprise import Dataset, Reader
import pandas as pd


# Load ratings/users dataset (adjust the file path accordingly)
ratings_df = pd.read_csv("ratings.csv")
users_df = pd.read_csv("users.csv")
courses_df = pd.read_csv("courses.csv")

# Prepare data for Surprise
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings_df[['user_id', 'course_id', 'rating']], reader)

# Split into training and testing sets
trainset, testset = surprise_train_test_split(data, test_size=0.2, random_state=42)

# Load the trained model
svd_model = joblib.load('course_recommender_model.pkl')

# Evaluate on the test set
predictions = svd_model.test(testset)
rmse = accuracy.rmse(predictions)
mae = accuracy.mae(predictions)
print(f"Test Set RMSE: {rmse:.4f}")
print(f"Test Set MAE: {mae:.4f}")

# Function to get top-N recommendations
def get_top_n_recommendations(predictions, n=10):
    # Map the predictions to each user
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))
    
    # Sort the predictions for each user and get top n
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    
    return top_n

# Generate top-10 recommendations for each user
top_n_predictions = get_top_n_recommendations(predictions, n=10)

# Compute precision and recall metrics
def precision_recall_at_k(predictions, k=10, threshold=3.5):
    """
    Return precision and recall at k metrics for each user
    """
    # First map the predictions to each user
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))
    
    precisions = dict()
    recalls = dict()
    
    for uid, user_ratings in user_est_true.items():
        # Sort user ratings by estimated value
        user_ratings.sort(key=lambda x: x[0], reverse=True)
        
        # Number of relevant items
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)
        
        # Number of recommended items in top k
        n_rec_k = min(k, len(user_ratings))
        
        # Number of relevant and recommended items in top k
        n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold)) 
                              for (est, true_r) in user_ratings[:n_rec_k])
        
        # Precision@K: Proportion of recommended items that are relevant
        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 0
        
        # Recall@K: Proportion of relevant items that are recommended
        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 0
    
    return precisions, recalls

# Calculate precision and recall at k=10
precisions, recalls = precision_recall_at_k(predictions, k=10, threshold=4.0)

# Calculate average precision and recall
avg_precision = sum(prec for prec in precisions.values()) / len(precisions)
avg_recall = sum(rec for rec in recalls.values()) / len(recalls)

print(f"Average Precision@10: {avg_precision:.4f}")
print(f"Average Recall@10: {avg_recall:.4f}")

# Role-based recommendation analysis
users_with_roles = pd.merge(
    pd.DataFrame(list(top_n_predictions.items()), columns=['user_id', 'recommendations']),
    users_df,
    on='user_id'
)

# Extract recommended course IDs
users_with_roles['recommended_course_ids'] = users_with_roles['recommendations'].apply(
    lambda x: [int(course_id) for course_id, _ in x]
)

# Get course types for recommended courses
role_recommendations = {}
for role in users_df['role'].unique():
    role_users = users_with_roles[users_with_roles['role'] == role]
    recommended_courses = [course for user_courses in role_users['recommended_course_ids'] for course in user_courses]
    course_types = courses_df[courses_df['course_id'].isin(recommended_courses)]['type'].value_counts(normalize=True)
    role_recommendations[role] = course_types.to_dict()

# Visualize role-based recommendations
role_rec_df = pd.DataFrame(role_recommendations).fillna(0).T
plt.figure(figsize=(14, 10))
sns.heatmap(role_rec_df, annot=True, cmap='viridis', fmt='.2f')
plt.title('Proportion of Course Types Recommended by Role')
plt.tight_layout()
plt.savefig('role_based_recommendations.png')

print("Model evaluation completed")