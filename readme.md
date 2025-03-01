Step 1: Create Folder and Open in VS Code
Step 2: Open terminal and Create/activate virtual env using this 
cmd --> python -m venv myenv
cmd --> myenv\Scripts\activate
Step 3: Create requirements.txt for installing project dependency pacakages using this
cmd --> pip install requirements.txt
Step 4: Collect Data and Store inside the project folder or Create Python Script synthetic_data.py to generate Synthetic data and save the files in csv format users.csv, courses.csv, ratings.csv
Step 5: Start Doing Exploratory Data Analysis with your synthetic datas
Step 6: Start Building Recommendation model with SVD algorithm (Collaborative Filtering) and save model as pkl file
Step 7: Start Evaluating Model by Metrics
Step 8: Start Build your flask app script app.py and frontend in templates folder index.html
Step 9: Create Dockefile
Step 10: Build Docker image using this 
cmd --> docker build -t flask-app .
Step 11: Run the container using this
cmd --> docker run -p 5000:5000 flask-app