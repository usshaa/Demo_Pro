import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load the data
users_df = pd.read_csv('users.csv')
courses_df = pd.read_csv('courses.csv')
ratings_df = pd.read_csv('ratings.csv')

print("Dataset Overview:")
print(f"Number of users: {len(users_df)}")
print(f"Number of courses: {len(courses_df)}")
print(f"Number of ratings: {len(ratings_df)}")
print(f"Rating density: {len(ratings_df) / (len(users_df) * len(courses_df)) * 100:.2f}%")

# Distribution of users by role
plt.figure(figsize=(12, 6))
sns.countplot(x='role', data=users_df)
plt.title('Distribution of Users by IT Role')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('user_role_distribution.png')

# Distribution of courses by type
plt.figure(figsize=(12, 6))
sns.countplot(x='type', data=courses_df)
plt.title('Distribution of Courses by Type')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('course_type_distribution.png')

# Distribution of ratings
plt.figure(figsize=(10, 6))
sns.histplot(ratings_df['rating'], bins=9, kde=True)
plt.title('Distribution of Course Ratings')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.savefig('rating_distribution.png')

# Average rating by course type
avg_rating_by_type = courses_df.groupby('type')['avg_rating'].mean().sort_values(ascending=False)
plt.figure(figsize=(12, 6))
avg_rating_by_type.plot(kind='bar')
plt.title('Average Rating by Course Type')
plt.xlabel('Course Type')
plt.ylabel('Average Rating')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('avg_rating_by_course_type.png')

# Create a pivot table for user-course ratings
user_course_matrix = ratings_df.pivot(index='user_id', columns='course_id', values='rating')
print(f"Sparsity of user-course matrix: {user_course_matrix.isna().sum().sum() / (user_course_matrix.shape[0] * user_course_matrix.shape[1]) * 100:.2f}%")

# Role-based course preference analysis
role_course_ratings = pd.merge(ratings_df, users_df, on='user_id')
role_course_ratings = pd.merge(role_course_ratings, courses_df, on='course_id')

avg_rating_by_role_type = role_course_ratings.groupby(['role', 'type'])['rating'].mean().reset_index()
plt.figure(figsize=(14, 8))
sns.heatmap(avg_rating_by_role_type.pivot(index='role', columns='type', values='rating'), annot=True, cmap='viridis')
plt.title('Average Rating by Role and Course Type')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('role_course_preference.png')

print("EDA completed and visualizations saved")