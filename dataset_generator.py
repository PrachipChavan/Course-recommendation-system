import pandas as pd
import random
import os

# Set seed for reproducibility
random.seed(42)

# Define domains and matching data
domains_data = {
    "Web Development": {
        "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Express", "MongoDB", "SQL", "Tailwind CSS", "TypeScript", "Next.js", "Git", "REST APIs"],
        "instructors": ["Colt Steele", "Angela Yu", "Maximilian Schwarzmüller", "Jonas Schmedtmann", "Brad Traversy"],
        "templates": [
            ("The Complete {skill} Bootcamp", "Master {skill} from scratch. Learn building modern, responsive, and interactive applications using industry best practices."),
            ("Advanced {skill} and Design Patterns", "Deep dive into {skill}. Learn performance optimization, security, state management, and enterprise-level architecture."),
            ("Build Real-World Projects with {skill}", "An entirely project-based course where you will build 10+ professional applications using {skill} and modern tools."),
            ("{skill} for Beginners: Start Coding Today", "Learn the fundamentals of {skill}. Perfect for absolute beginners with no prior coding experience."),
            ("Full-Stack Web Dev with React and {skill}", "Become a full-stack engineer. Build robust backends and dynamic frontends using React and {skill}.")
        ]
    },
    "Data Science & Analytics": {
        "skills": ["Python", "Pandas", "NumPy", "SQL", "Tableau", "Power BI", "Exploratory Data Analysis", "Statistics", "Data Visualization", "Excel", "R Programming"],
        "instructors": ["Kirill Eremenko", "Jose Portilla", "Andrew Ng", "Daniel Bourke", "Alex The Analyst"],
        "templates": [
            ("Data Science Masterclass: {skill} & Statistics", "Learn how to clean, analyze, and visualize data using {skill}. Covers statistical modeling and business intelligence."),
            ("Interactive Data Visualization with {skill}", "Transform raw data into beautiful, interactive dashboards and stories using {skill} and storytelling techniques."),
            ("SQL & {skill} for Data Analysts", "Master database querying and data wrangling with SQL and {skill}. Solve real-world business analytics problems."),
            ("Business Intelligence using {skill}", "Drive data-driven decisions. Learn advanced reporting, cohort analysis, and predictive modeling using {skill}."),
            ("{skill} Boot Camp: Go from Zero to Hero", "A comprehensive guide to analyzing data. Learn data frames, wrangling, and basic predictive analytics with {skill}.")
        ]
    },
    "AI & Machine Learning": {
        "skills": ["Machine Learning", "Deep Learning", "Neural Networks", "PyTorch", "TensorFlow", "NLP", "Computer Vision", "Scikit-learn", "Generative AI", "LLMs", "Reinforcement Learning"],
        "instructors": ["Andrew Ng", "Lazy Programmer", "Andrej Karpathy", "Daniel Bourke", "Sam Witteveen"],
        "templates": [
            ("Introduction to {skill} & Neural Networks", "Understand the mathematical foundations and core concepts behind modern {skill} algorithms."),
            ("Practical {skill} with PyTorch and Scikit-Learn", "Build, train, and deploy powerful {skill} models for classification, regression, and clustering tasks."),
            ("Advanced {skill}: Deep Dive & Research", "Explore cutting-edge techniques in {skill}, including architecture design, hyperparameter tuning, and model optimization."),
            ("Generative AI & {skill} Application Development", "Learn to build applications powered by Large Language Models and custom {skill} agents."),
            ("Computer Vision & NLP using {skill}", "Process images, video, and natural language text using advanced {skill} frameworks and pre-trained models.")
        ]
    },
    "Cloud Computing & DevOps": {
        "skills": ["AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "CI/CD", "Terraform", "Linux", "Shell Scripting", "Ansible", "Jenkins"],
        "instructors": ["Stephane Maarek", "Adrian Cantrill", "Mumshad Mannambeth", "Nigel Poulton", "Richard Chan"],
        "templates": [
            ("{skill} Certified Solutions Architect", "Prepare and pass the official certification. Master core services, security, architecture, and cost optimization on {skill}."),
            ("DevOps Essentials: {skill} & CI/CD Pipelines", "Automate your infrastructure, deployment, and testing lifecycle using {skill} and modern pipelines."),
            ("Containerization with Docker & {skill} Masterclass", "Learn to package, deploy, and scale microservices using Docker and {skill} orchestration in production."),
            ("Infrastructure as Code using Terraform and {skill}", "Provision and manage cloud resources programmatically across multi-cloud setups with Terraform and {skill}."),
            ("Advanced System Administration & {skill}", "Master Linux command line, shell scripting, automation, and system security with a focus on {skill} services.")
        ]
    },
    "Cybersecurity": {
        "skills": ["Network Security", "Penetration Testing", "Cryptography", "Ethical Hacking", "Linux", "Wireshark", "Metasploit", "Security Fundamentals", "Incident Response"],
        "instructors": ["Nathan House", "Heath Adams", "Jason Dion", "Alexis Ahmed", "Neal Bridges"],
        "templates": [
            ("The Complete Ethical Hacking Course: {skill}", "Learn how to think like a hacker. Perform vulnerability scans, exploit targets, and secure systems using {skill}."),
            ("{skill} & CompTIA Security+ Prep Course", "Master core cybersecurity concepts, threats, mitigation strategies, and get fully prepared for your certification in {skill}."),
            ("Advanced Penetration Testing & {skill}", "Go deep into red teaming tactics. Conduct advanced assessments, write custom exploits, and bypass security controls using {skill}."),
            ("Network Defense & {skill} Analysis", "Learn network traffic analysis, intrusion detection, firewalls, and security operations using {skill}."),
            ("Incident Response & {skill} Operations", "Detect, isolate, and mitigate active cybersecurity incidents. Learn digital forensics and blue team tactics for {skill}.")
        ]
    },
    "Mobile App Development": {
        "skills": ["Flutter", "React Native", "Swift", "Kotlin", "iOS Development", "Android Development", "Dart", "Xcode", "Firebase", "Mobile UI Design"],
        "instructors": ["Angela Yu", "Maximilian Schwarzmüller", "Stephen Grider", "Philipp Lackner", "Paul Hudson"],
        "templates": [
            ("iOS & Android Development with {skill}", "Build beautiful, native cross-platform mobile apps for iOS and Android using a single codebase of {skill}."),
            ("Complete {skill} Developer Bootcamp", "Learn mobile application development from scratch. Design layouts, manage state, and deploy to App Store and Google Play."),
            ("Advanced State Management in {skill} Apps", "Build robust, testable, and production-ready mobile architectures using {skill} state management and testing frameworks."),
            ("Build a Social Media App with {skill} and Firebase", "Integrate databases, authentication, storage, and push notifications into your {skill} app using Firebase backend services."),
            ("{skill} UI/UX: Design and Animation Masterclass", "Create stunning user interfaces, custom transitions, and fluid animations in your {skill} applications.")
        ]
    },
    "Business & Product Management": {
        "skills": ["Product Management", "Agile Methodology", "Scrum", "Project Management", "Finance", "Startup Strategy", "Leadership", "Business Strategy", "Negotiation"],
        "instructors": ["Cole Mercer", "Evan Kimbrell", "Seth Godin", "Todd Birzer", "Mary Pratt"],
        "templates": [
            ("Become a Product Manager: {skill} and Analytics", "Learn the product lifecycle, market research, user personas, agile delivery, and metrics definition for {skill}."),
            ("Agile & Scrum Master certification: {skill}", "Master agile ceremonies, sprint planning, backlog grooming, and team leadership using Scrum and {skill}."),
            ("Project Management Professional (PMP) Prep with {skill}", "Comprehensive training on predictive, agile, and hybrid project frameworks. Includes mock exams covering {skill}."),
            ("Startup Foundations: {skill} & Lean Canvas", "How to validate ideas, raise capital, design business models, and execute go-to-market strategies using {skill}."),
            ("Strategic Leadership and {skill} for Executives", "Develop decision-making models, corporate strategy, and negotiation skills to lead high-performing teams in {skill} contexts.")
        ]
    },
    "UI/UX & Product Design": {
        "skills": ["Figma", "Adobe XD", "Wireframing", "Prototyping", "User Research", "Interaction Design", "Visual Design", "Usability Testing", "Design Systems"],
        "instructors": ["Daniel Walter Scott", "Muzli Academy", "Sarah Gibbons", "Zack Onisko", "Jesse Showalter"],
        "templates": [
            ("User Experience Design Essentials: {skill}", "Learn UX research, user journeys, wireframing, prototyping, and usability testing in {skill}."),
            ("Mastering Figma: Design Systems & Auto-Layout", "Create robust, scalable design systems, components, variants, and interactive prototypes using {skill} like a pro."),
            ("Interface Design & Typography with {skill}", "Elevate your visual design skills. Master grid layouts, color theory, and typographic hierarchy using {skill}."),
            ("User Research and Usability Testing in Practice", "Plan, conduct, and analyze user research and usability sessions. Turn feedback into mockups with {skill}."),
            ("Mobile and Web UI Design Bootcamp with {skill}", "Design gorgeous, high-fidelity responsive websites and mobile app layouts using {skill} for client handoff.")
        ]
    },
    "Digital Marketing": {
        "skills": ["SEO", "Google Analytics", "Content Marketing", "Social Media Marketing", "Email Marketing", "Copywriting", "Growth Hacking", "Facebook Ads", "Google Ads"],
        "instructors": ["Alex Cattoni", "Neil Patel", "Isaac Rudansky", "Robin & Jesper", "Daragh Walsh"],
        "templates": [
            ("Digital Marketing Masterclass: {skill} & Branding", "Grow your business online. Master SEO, social media, paid ads, and analytics using {skill} tools."),
            ("The Ultimate {skill} Guide to Page #1", "Rank higher on search engines. Master on-page, off-page, technical optimizations, and keyword research using {skill}."),
            ("Google Analytics 4 & {skill} Data Analysis", "Track user behavior, measure conversions, set up custom dashboards, and make data-driven marketing decisions with {skill}."),
            ("Copywriting & {skill} for Maximum Conversions", "Write persuasive copy for emails, sales pages, and social media. Combine copywriting with {skill} metrics."),
            ("Growth Hacking & Viral Marketing with {skill}", "Acquire customers at scale. Implement loops, referral programs, and rapid A/B testing utilizing {skill} channels.")
        ]
    }
}

# Platforms list
platforms = ["Udemy", "Coursera", "edX", "Pluralsight", "Udacity"]
levels = ["Beginner", "Intermediate", "Advanced"]

def generate_courses(n=200):
    courses = []
    
    for i in range(1, n + 1):
        domain = random.choice(list(domains_data.keys()))
        domain_info = domains_data[domain]
        
        # Pick 2-4 random skills from the domain to associate with the course
        num_skills = random.randint(2, 4)
        course_skills = random.sample(domain_info["skills"], min(num_skills, len(domain_info["skills"])))
        primary_skill = course_skills[0]
        
        # Generate title and description using a random template
        template_title, template_desc = random.choice(domain_info["templates"])
        title = template_title.format(skill=primary_skill)
        description = template_desc.format(skill=primary_skill)
        
        # Add other skills to the description or tags to make the description richer
        skills_str = ", ".join(course_skills)
        description += f" Topics include: {skills_str}."
        
        # Instructor
        instructor = random.choice(domain_info["instructors"])
        
        # Platform
        platform = random.choice(platforms)
        
        # Rating & Reviews (making popular courses have more reviews and higher ratings)
        base_rating = random.choice([3.8, 4.0, 4.2, 4.5, 4.7, 4.8])
        rating = round(min(5.0, base_rating + random.uniform(-0.1, 0.2)), 2)
        reviews_count = int(random.lognormvariate(mu=6.5, sigma=1.2)) # lognormal to simulate a few highly popular courses
        
        # Difficulty Level
        level = random.choice(levels)
        
        # Duration (hours)
        if level == "Beginner":
            duration = round(random.uniform(4.0, 15.0), 1)
        elif level == "Intermediate":
            duration = round(random.uniform(10.0, 35.0), 1)
        else: # Advanced
            duration = round(random.uniform(20.0, 65.0), 1)
            
        courses.append({
            "Course ID": f"CRS-{i:03d}",
            "Title": title,
            "Description": description,
            "Domain": domain,
            "Difficulty Level": level,
            "Rating": rating,
            "Number of Reviews": reviews_count,
            "Duration (Hours)": duration,
            "Instructor": instructor,
            "Platform": platform,
            "Skills": skills_str
        })
        
    df = pd.DataFrame(courses)
    return df

if __name__ == "__main__":
    output_dir = r"C:\Users\Prachi\Desktop\courses_data" # Let's keep it in the project workspace
    project_dir = r"C:\Users\Prachi\.gemini\antigravity\scratch\course_recommendation_system"
    
    os.makedirs(project_dir, exist_ok=True)
    csv_path = os.path.join(project_dir, "courses_dataset.csv")
    
    df = generate_courses(220) # Generate 220 courses
    df.to_csv(csv_path, index=False)
    print(f"Generated dataset with {len(df)} courses at: {csv_path}")
