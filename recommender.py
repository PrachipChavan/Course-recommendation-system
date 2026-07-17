import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Standard roles and their required skills
CAREER_ROLES = {
    "Full Stack Developer": [
        "HTML", "CSS", "JavaScript", "React", "Node.js", "Express", 
        "MongoDB", "SQL", "Tailwind CSS", "TypeScript", "Next.js", "Git", "REST APIs"
    ],
    "Data Scientist": [
        "Python", "Pandas", "NumPy", "SQL", "Tableau", "Power BI", 
        "Exploratory Data Analysis", "Statistics", "Data Visualization", "Excel", "R Programming"
    ],
    "AI/ML Engineer": [
        "Python", "Machine Learning", "Deep Learning", "Neural Networks", "PyTorch", 
        "TensorFlow", "NLP", "Computer Vision", "Scikit-learn", "Generative AI", "LLMs"
    ],
    "DevOps Engineer": [
        "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "CI/CD", 
        "Terraform", "Linux", "Shell Scripting", "Ansible", "Jenkins"
    ],
    "Cybersecurity Analyst": [
        "Network Security", "Penetration Testing", "Cryptography", "Ethical Hacking", 
        "Linux", "Wireshark", "Metasploit", "Security Fundamentals", "Incident Response"
    ],
    "Mobile App Developer": [
        "Flutter", "React Native", "Swift", "Kotlin", "iOS Development", 
        "Android Development", "Dart", "Firebase", "Mobile UI Design"
    ],
    "Product Manager": [
        "Product Management", "Agile Methodology", "Scrum", "Project Management", 
        "Finance", "Startup Strategy", "Leadership", "Business Strategy", "Negotiation"
    ],
    "UI/UX Designer": [
        "Figma", "Adobe XD", "Wireframing", "Prototyping", "User Research", 
        "Interaction Design", "Visual Design", "Usability Testing", "Design Systems"
    ],
    "Digital Marketer": [
        "SEO", "Google Analytics", "Content Marketing", "Social Media Marketing", 
        "Email Marketing", "Facebook Ads", "Google Ads", "Growth Hacking", "Copywriting"
    ]
}

class CourseRecommender:
    def __init__(self, dataset_path):
        self.df = pd.read_csv(dataset_path)
        # Handle empty/missing values
        self.df["Title"] = self.df["Title"].fillna("")
        self.df["Description"] = self.df["Description"].fillna("")
        self.df["Domain"] = self.df["Domain"].fillna("")
        self.df["Skills"] = self.df["Skills"].fillna("")
        
        # Combine text columns for TF-IDF mapping
        self.df["combined_text"] = (
            self.df["Title"] + " " +
            self.df["Description"] + " " +
            self.df["Domain"] + " " +
            self.df["Skills"]
        )
        
        # Initialize and fit TF-IDF
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["combined_text"])
        
    def get_recommendations(self, query, top_n=5, difficulty=None, duration_range=None, platforms=None, min_rating=0.0):
        """
        Gets content-based recommendations based on user search query or user profile description.
        """
        if not query.strip():
            # If query is empty, return top rated courses as fallback
            filtered_df = self.df.copy()
        else:
            # Transform user query
            query_vec = self.vectorizer.transform([query])
            # Compute cosine similarity
            similarity_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            
            # Add similarity score to df
            filtered_df = self.df.copy()
            filtered_df["Similarity Score"] = similarity_scores
            
            # Sort by similarity score descending
            filtered_df = filtered_df.sort_values(by="Similarity Score", ascending=False)
            
        # Apply filters
        if difficulty and difficulty != "All":
            filtered_df = filtered_df[filtered_df["Difficulty Level"] == difficulty]
            
        if duration_range:
            min_dur, max_dur = duration_range
            filtered_df = filtered_df[(filtered_df["Duration (Hours)"] >= min_dur) & (filtered_df["Duration (Hours)"] <= max_dur)]
            
        if platforms and len(platforms) > 0:
            filtered_df = filtered_df[filtered_df["Platform"].isin(platforms)]
            
        if min_rating > 0.0:
            filtered_df = filtered_df[filtered_df["Rating"] >= min_rating]
            
        return filtered_df.head(top_n)

    def analyze_skills_gap(self, current_skills_list, target_role):
        """
        Analyzes the gap between current skills and target role requirements, 
        and suggests courses to bridge this gap.
        """
        if target_role not in CAREER_ROLES:
            return None
            
        required_skills = CAREER_ROLES[target_role]
        
        # Normalize lists for comparison
        clean_current = [s.strip().lower() for s in current_skills_list if s.strip()]
        
        acquired = []
        missing = []
        
        for skill in required_skills:
            if skill.lower() in clean_current:
                acquired.append(skill)
            else:
                missing.append(skill)
                
        # Calculate progress percentage
        total_req = len(required_skills)
        progress_pct = int(len(acquired) / total_req * 100) if total_req > 0 else 100
        
        # For each missing skill, find the best course
        gap_recommendations = {}
        for skill in missing:
            # Look for courses where the skill is explicitly mentioned in the 'Skills' tag
            # or use tf-idf similarity with the skill name as query
            skill_esc = re.escape(skill)
            pattern = rf"\b{skill_esc}\b"
            exact_matches = self.df[self.df["Skills"].str.contains(pattern, case=False, na=False)]
            
            if not exact_matches.empty:
                # Sort by rating and review count
                best_course = exact_matches.sort_values(by=["Rating", "Number of Reviews"], ascending=False).iloc[0]
            else:
                # Fallback to TF-IDF search
                query_vec = self.vectorizer.transform([skill])
                scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
                best_idx = np.argmax(scores)
                best_course = self.df.iloc[best_idx]
                
            gap_recommendations[skill] = best_course.to_dict()
            
        return {
            "required_skills": required_skills,
            "acquired_skills": acquired,
            "missing_skills": missing,
            "progress_percentage": progress_pct,
            "recommendations": gap_recommendations
        }
