
# MeaLit 2.0 - Visual Food Recommendation Engine
MeaLit 2.0 is a web-based food recommendation engine that provides personalized restaurant and recipe recommendations based on user preferences. The application allows users to register and log in to take a preference quiz and receive recommendations based on their answers. MeaLit 2.0 also improves recommendations based on a user's search history.

The project is built using HTML, CSS, Bootstrap, JavaScript, Flask, SQLite, and web-scraping tools such as Beautiful Soup and Selenium.

## Getting Started


1. Clone the repository:
```
 git clone https://github.com/Soumya-Vaidya/MeaLit-2.0.git
```

2. Navigate into the project directory
3. Install the required dependencies: 

```
pip install -r requirements.txt
```
4. To run the application, run the following command:
```
python app.py
```

This will start the Flask development server. You can access the application by navigating to http://localhost:8000/ in your web browser.


### OR Install Using Docker


1. 
```
docker build -t mealit2.0 https://github.com/Soumya-Vaidya/MeaLit-2.0.git
```

2.
```
docker run -p 8000:8000 mealit2.0
```



## Features
- User authentication (registration and login)
- Preference quiz for personalized recommendations
- Dynamic restaurant recommendation system
- Recipe recommendation based on available ingredients
- Categorization and saving of recommended restaurants and recipes (CRUD operations)
- Search history-based recommendation improvement
- Data web-scraping using Beautiful Soup and Selenium
- User-friendly interface with visually appealing design

## Description

### Register and Login
To use the MeaLit 2.0 recommendation engine, users must first register and log in. Click on the "Register" button to create an account or "Login" if you already have one.

### Preference Quiz
After logging in, users will be directed to the preference quiz. The quiz consists of questions related to food preferences such as cuisine, location, and budget. Based on the user's answers, the system will provide restaurant and recipe recommendations tailored to their preferences.

### Restaurant Recommendations
Once the preference quiz is completed, the user will receive restaurant recommendations based on their answers. The recommendations will include details such as the restaurant's name, cuisine, location, price range, and user ratings. Users can also categorize and save their favorite restaurants for future reference.

### Recipe Recommendations
Users can also receive recipe recommendations based on the ingredients they have on hand. The recipe recommendations will include the recipe name, ingredients, and cooking instructions.

### Search History and Recommendation Improvement
MeaLit 2.0 improves recommendations based on a user's search history. The system will keep track of a user's search history and use it to refine future recommendations.

### Popular Recipes and Restaurants
MeaLit 2.0 includes a "Popular" section that displays the most popular recipes and restaurants among all users. This section provides users with inspiration for their next meal and introduces them to new places to eat and cook.

## Technology Stack
Quantified Self is built using the following technologies:

Front-end: HTML, CSS, JavaScript, Bootstrap

Back-end: Python Flask

Database: SQLite

Web Scraping: Beautiful Soup, Selenium

## Credits

This project was made by Soumya Vaidya and Anushka Bhatnagar.

Recipie Reccomendation System : https://github.com/SaloniGandhi/Recipes-Recommender.git

