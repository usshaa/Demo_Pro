from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split as surprise_train_test_split
from surprise.model_selection import GridSearchCV
import joblib
import pandas as pd

# Load ratings dataset (adjust the file path accordingly)
ratings_df = pd.read_csv("ratings.csv")

# Prepare data for Surprise
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings_df[['user_id', 'course_id', 'rating']], reader)

# Split into training and testing sets
trainset, testset = surprise_train_test_split(data, test_size=0.2, random_state=42)

# Tune the SVD model parameters using grid search
param_grid = {
    'n_factors': [50, 100, 150],
    'n_epochs': [20, 30],
    'lr_all': [0.005, 0.01],
    'reg_all': [0.02, 0.05]
}

gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
gs.fit(data)

print("Best RMSE:", gs.best_score['rmse'])
print("Best parameters:", gs.best_params['rmse'])

# Train the model with the best parameters
best_params = gs.best_params['rmse']
svd_model = SVD(
    n_factors=best_params['n_factors'], 
    n_epochs=best_params['n_epochs'], 
    lr_all=best_params['lr_all'], 
    reg_all=best_params['reg_all']
)
svd_model.fit(trainset)

# Save the trained model
joblib.dump(svd_model, 'course_recommender_model.pkl')
print("Model trained and saved")