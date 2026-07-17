# EduMatch AI: Course Recommendation & Skills-Gap Planner 🎓
<img width="1912" height="852" alt="Screenshot 2026-07-17 162825" src="https://github.com/user-attachments/assets/2b070281-00f8-46cc-bfec-0956d429c773" />

EduMatch AI is a modern, interactive web application built with **Streamlit**, **scikit-learn**, and **Plotly**. It serves as an intelligent course recommendation engine and a career roadmap planner, designed to help users identify their current skills, target a specific career track, analyze their skills gap, and discover the exact courses needed to bridge that gap.

---

## 🚀 Key Features

### 1. 📊 Catalog Insights & Analytics
* **Dashboard Summary**: Real-time stats on total courses, average rating, duration, and reviews.
* **Interactive Visuals (Plotly)**:
  * **Domain distribution**: Overview of course availability across multiple fields.
  * **Platform split**: Distribution of courses across platforms like Udemy, Coursera, edX, Pluralsight, and Udacity.
  * **Rating vs. Duration Scatter Plot**: Bubble chart visualizing course rating and duration, sized by review counts and colored by difficulty.
  * **Ratings Comparison**: Multi-variable analysis comparing ratings by platform and difficulty levels.

### 2. 🎯 Smart Course Finder
* **Semantic Search**: Text-based query system powered by **TF-IDF (Term Frequency-Inverse Document Frequency) Vectorization** and **Cosine Similarity** to match user queries with course titles, descriptions, and tags.
* **Granular Filtering**: Filter recommendations dynamically by:
  * Difficulty level (*Beginner, Intermediate, Advanced*)
  * Duration range (in hours)
  * Platform (*Udemy, Coursera, edX, etc.*)
  * Minimum course rating
* **Interactive Cards**: High-end glassmorphism cards presenting course metadata, teaching tags, platforms, and interactive similarity match scores.

### 3. 🛣️ Career Skills-Gap Planner
* **Role Modeling**: Select from 9 predefined career roles:
  * *Full Stack Developer*
  * *Data Scientist*
  * *AI/ML Engineer*
  * *DevOps Engineer*
  * *Cybersecurity Analyst*
  * *Mobile App Developer*
  * *Product Manager*
  * *UI/UX Designer*
  * *Digital Marketer*
* **Gap Analysis**: Compares your self-declared skills against target role requirements to calculate a readiness match score.
* **Tailored Roadmaps**: Breaks down your exact skills gap (missing skills) and maps them to a structured learning path with highly rated courses chosen directly from the database.

---

## 🛠️ Tech Stack
* **Frontend/Interface**: [Streamlit](https://streamlit.io/) (enhanced with custom CSS injects for modern glassmorphism aesthetic)
* **Algorithms & Machine Learning**: [scikit-learn](https://scikit-learn.org/) (TF-IDF vectorizer, Cosine Similarity matrices)
* **Data Visualization**: [Plotly Express & Plotly Graph Objects](https://plotly.com/)
* **Data Wrangling**: [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)

---

## 📦 Project Structure
```text
course_recommendation_system/
├── app.py                  # Streamlit frontend & interactive dashboard layout
├── recommender.py          # TF-IDF calculations & Career Skills-Gap logic
├── dataset_generator.py    # Generates a synthetic dataset of 220 courses
├── requirements.txt        # Python package dependencies
├── courses_dataset.csv     # The generated courses dataset
└── README.md               # Project documentation
