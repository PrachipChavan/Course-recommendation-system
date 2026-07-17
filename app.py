import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from recommender import CourseRecommender, CAREER_ROLES

# Set page config
st.set_page_config(
    page_title="EduMatch | AI Course Recommendation & Skills Planner",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Apply modern typography and background */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Background gradient */
.stApp {
    background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e1b4b 100%);
    color: #f3f4f6;
}

/* Glassmorphic cards for courses */
.course-card {
    background: rgba(17, 24, 39, 0.6);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 24px;
    margin-bottom: 24px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
}

.course-card:hover {
    transform: translateY(-6px);
    border-color: rgba(99, 102, 241, 0.4);
    box-shadow: 0 12px 30px rgba(99, 102, 241, 0.15);
    background: rgba(17, 24, 39, 0.85);
}

/* Domain and tags */
.domain-badge {
    background-color: rgba(99, 102, 241, 0.15);
    color: #a5b4fc;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: inline-block;
    margin-bottom: 12px;
    border: 1px solid rgba(99, 102, 241, 0.3);
}

.platform-badge {
    background-color: rgba(244, 63, 94, 0.15);
    color: #fda4af;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: inline-block;
    margin-bottom: 12px;
    margin-left: 6px;
    border: 1px solid rgba(244, 63, 94, 0.3);
}

.difficulty-badge {
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: inline-block;
    margin-bottom: 12px;
    margin-left: 6px;
}

.difficulty-Beginner {
    background-color: rgba(16, 185, 129, 0.15);
    color: #6ee7b7;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.difficulty-Intermediate {
    background-color: rgba(245, 158, 11, 0.15);
    color: #fde047;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.difficulty-Advanced {
    background-color: rgba(239, 68, 68, 0.15);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.card-title {
    font-size: 20px;
    font-weight: 700;
    margin-top: 6px;
    margin-bottom: 8px;
    color: #ffffff;
    line-height: 1.3;
}

.card-instructor {
    color: #9ca3af;
    font-size: 13px;
    font-weight: 500;
    margin-bottom: 14px;
}

.card-desc {
    color: #d1d5db;
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 18px;
}

/* Skills section in card */
.skills-container {
    margin-bottom: 18px;
}

.skill-tag {
    background-color: rgba(255, 255, 255, 0.08);
    color: #e5e7eb;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 500;
    display: inline-block;
    margin-right: 6px;
    margin-bottom: 6px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding-top: 14px;
    margin-top: 14px;
}

.card-duration {
    color: #38bdf8;
    font-size: 13px;
    font-weight: 600;
    display: flex;
    align-items: center;
}

.card-rating-container {
    display: flex;
    align-items: center;
}

.star-rating {
    color: #fbbf24;
    font-size: 15px;
    margin-right: 5px;
}

.rating-number {
    font-weight: 700;
    color: #ffffff;
    font-size: 14px;
    margin-right: 4px;
}

.review-count {
    color: #9ca3af;
    font-size: 12px;
}

/* Metrics styles */
.metric-box {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.metric-title {
    color: #9ca3af;
    font-size: 13px;
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.metric-value {
    color: #ffffff;
    font-size: 28px;
    font-weight: 800;
    margin-top: 4px;
}

/* Skills gap container styling */
.gap-item {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 10px;
    padding: 14px;
    border-left: 4px solid #ef4444;
    margin-bottom: 12px;
}

.gap-item-acquired {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 10px;
    padding: 14px;
    border-left: 4px solid #10b981;
    margin-bottom: 12px;
}

/* Sidebar premium adjustments */
.sidebar .sidebar-content {
    background: #0b0f19;
}
</style>
""", unsafe_allow_html=True)

# Define paths
PROJECT_DIR = r"C:\Users\Prachi\.gemini\antigravity\scratch\course_recommendation_system"
DATASET_PATH = os.path.join(PROJECT_DIR, "courses_dataset.csv")

# Initialize recommender instance
@st.cache_resource
def get_recommender():
    if not os.path.exists(DATASET_PATH):
        # Fallback if csv doesn't exist (in case of wrong directory)
        return None
    return CourseRecommender(DATASET_PATH)

recommender = get_recommender()

if recommender is None:
    st.error("⚠️ Course dataset not found. Please run the `dataset_generator.py` script first.")
    st.stop()

# Header section
st.markdown("""
<div style='text-align: center; padding: 25px 0px 15px 0px;'>
    <h1 style='font-size: 3rem; font-weight: 800; background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        🎓 EduMatch AI
    </h1>
    <p style='color: #9ca3af; font-size: 1.15rem; max-width: 700px; margin: 10px auto;'>
        Discover personalized learning paths, bridge your technical skills gaps, and explore recommendations powered by intelligent content-based analysis.
    </p>
</div>
""", unsafe_allow_html=True)

# Helper function to render a course card in HTML
def render_course_card(course, sim_score=None):
    rating = course["Rating"]
    stars = "★" * int(round(rating)) + "☆" * (5 - int(round(rating)))
    
    # Clean float display
    duration = course["Duration (Hours)"]
    reviews = course["Number of Reviews"]
    
    skills_tags = "".join([f'<span class="skill-tag">{s.strip()}</span>' for s in str(course["Skills"]).split(",")])
    
    sim_score_html = ""
    if sim_score is not None:
        sim_score_html = f'<div style="color: #a855f7; font-size: 13px; font-weight: 700; margin-top: 5px;">🔥 Match Score: {int(sim_score * 100)}%</div>'

    html_content = f"""
    <div class="course-card">
        <div style="display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap;">
            <div>
                <span class="domain-badge">{course['Domain']}</span>
                <span class="platform-badge">{course['Platform']}</span>
                <span class="difficulty-badge difficulty-{course['Difficulty Level']}">{course['Difficulty Level']}</span>
            </div>
            {sim_score_html}
        </div>
        <div class="card-title">{course['Title']}</div>
        <div class="card-instructor">Instructor: <b>{course['Instructor']}</b></div>
        <div class="card-desc">{course['Description']}</div>
        <div class="skills-container">
            <div style="font-size: 12px; font-weight: 600; color: #9ca3af; margin-bottom: 6px;">SKILLS TAUGHT:</div>
            {skills_tags}
        </div>
        <div class="card-footer">
            <div class="card-duration">
                ⏱️ {duration} hours
            </div>
            <div class="card-rating-container">
                <span class="star-rating">{stars}</span>
                <span class="rating-number">{rating}</span>
                <span class="review-count">({reviews:,} reviews)</span>
            </div>
        </div>
    </div>
    """
    return html_content

# Create layout tabs
tab_dash, tab_rec, tab_gap = st.tabs([
    "📊 Catalog Insights & Analytics", 
    "🎯 Smart Course Finder", 
    "🛣️ Career Skills-Gap Planner"
])

# ----------------- TAB 1: DASHBOARD & ANALYTICS -----------------
with tab_dash:
    st.markdown("### 📈 Course Catalog Analytics")
    
    # Summary Metrics Row
    df = recommender.df
    total_courses = len(df)
    avg_rating = round(df["Rating"].mean(), 2)
    avg_duration = round(df["Duration (Hours)"].mean(), 1)
    total_reviews = df["Number of Reviews"].sum()
    
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">📚 Total Courses</div>
            <div class="metric-value">{total_courses}</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">⭐ Average Rating</div>
            <div class="metric-value">{avg_rating} / 5.0</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">⏱️ Avg Duration</div>
            <div class="metric-value">{avg_duration} hrs</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">💬 Total Reviews</div>
            <div class="metric-value">{total_reviews:,}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graphs Row 1
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        # Domain distribution
        domain_counts = df["Domain"].value_counts().reset_index()
        domain_counts.columns = ["Domain", "Count"]
        fig_domain = px.bar(
            domain_counts, 
            y="Domain", 
            x="Count", 
            orientation="h",
            title="Course Catalog Count by Domain",
            labels={"Count": "Number of Courses"},
            color="Count",
            color_continuous_scale="Viridis",
            template="plotly_dark"
        )
        fig_domain.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family="Plus Jakarta Sans",
            margin=dict(l=20, r=20, t=40, b=20),
            height=350
        )
        st.plotly_chart(fig_domain, use_container_width=True)
        
    with g_col2:
        # Platform split
        platform_counts = df["Platform"].value_counts().reset_index()
        platform_counts.columns = ["Platform", "Count"]
        fig_platform = px.pie(
            platform_counts, 
            values="Count", 
            names="Platform", 
            hole=0.4,
            title="Course Distribution by Platform",
            color_discrete_sequence=px.colors.sequential.RdBu,
            template="plotly_dark"
        )
        fig_platform.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family="Plus Jakarta Sans",
            margin=dict(l=20, r=20, t=40, b=20),
            height=350
        )
        st.plotly_chart(fig_platform, use_container_width=True)
        
    # Graphs Row 2
    g_col3, g_col4 = st.columns(2)
    
    with g_col3:
        # Scatter: Rating vs Duration colored by Difficulty
        fig_scatter = px.scatter(
            df,
            x="Duration (Hours)",
            y="Rating",
            color="Difficulty Level",
            hover_name="Title",
            size="Number of Reviews",
            size_max=35,
            title="Duration vs Rating (Size relative to Reviews Count)",
            color_discrete_map={"Beginner": "#4ade80", "Intermediate": "#facc15", "Advanced": "#fca5a5"},
            template="plotly_dark"
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family="Plus Jakarta Sans",
            margin=dict(l=20, r=20, t=40, b=20),
            height=380
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with g_col4:
        # Average rating by Platform & Difficulty
        avg_rating_platform = df.groupby(["Platform", "Difficulty Level"])["Rating"].mean().reset_index()
        fig_grouped = px.bar(
            avg_rating_platform,
            x="Platform",
            y="Rating",
            color="Difficulty Level",
            barmode="group",
            title="Average Course Rating by Platform & Difficulty Level",
            color_discrete_map={"Beginner": "#10b981", "Intermediate": "#f59e0b", "Advanced": "#ef4444"},
            template="plotly_dark"
        )
        fig_grouped.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family="Plus Jakarta Sans",
            yaxis=dict(range=[3.5, 5.0]),
            margin=dict(l=20, r=20, t=40, b=20),
            height=380
        )
        st.plotly_chart(fig_grouped, use_container_width=True)


# ----------------- TAB 2: SMART COURSE FINDER -----------------
with tab_rec:
    st.markdown("### 🔍 Find Your Perfect Course")
    
    # Layout sidebar and search results
    r_col1, r_col2 = st.columns([1, 3])
    
    with r_col1:
        st.markdown("#### 🛠️ Filters")
        
        # Search text
        search_query = st.text_input("Enter Skills, Interests, or Keywords:", placeholder="e.g. React Native, Machine Learning, UI design")
        
        # Difficulty selection
        difficulty_filter = st.selectbox("Difficulty Level:", ["All", "Beginner", "Intermediate", "Advanced"])
        
        # Rating filter
        rating_filter = st.slider("Minimum Course Rating:", 0.0, 5.0, 4.0, 0.1)
        
        # Duration slider
        max_dur_limit = float(df["Duration (Hours)"].max())
        min_dur_limit = float(df["Duration (Hours)"].min())
        duration_filter = st.slider("Course Duration (Hours):", min_dur_limit, max_dur_limit, (min_dur_limit, max_dur_limit))
        
        # Platform multi-select
        platforms_list = list(df["Platform"].unique())
        selected_platforms = st.multiselect("Platforms:", platforms_list, default=platforms_list)
        
        # Number of recommendations
        rec_count = st.slider("Number of recommendations to show:", 3, 15, 6)
        
    with r_col2:
        st.markdown(f"#### 💡 Top Recommendations for: *{search_query if search_query else 'General Catalog'}*")
        
        # Fetch recommendations
        recs = recommender.get_recommendations(
            query=search_query,
            top_n=rec_count,
            difficulty=difficulty_filter,
            duration_range=duration_filter,
            platforms=selected_platforms,
            min_rating=rating_filter
        )
        
        if recs.empty:
            st.info("No courses match your active filter criteria. Try expanding your search queries or lowering filter constraints.")
        else:
            for idx, row in recs.iterrows():
                sim = row.get("Similarity Score") if "Similarity Score" in recs.columns else None
                st.markdown(render_course_card(row, sim), unsafe_allow_html=True)


# ----------------- TAB 3: CAREER SKILLS GAP PLANNER -----------------
with tab_gap:
    st.markdown("### 🛣️ Career Path & Skills-Gap Planner")
    
    st.markdown("""
    Select your target role, configure the skills you currently possess, and our AI recommender will map out your exact skills gap and outline the custom courses required to fill it!
    """)
    
    # Inputs row
    gap_col1, gap_col2 = st.columns([1, 1])
    
    with gap_col1:
        target_role_selected = st.selectbox(
            "Select Target Career Role:",
            list(CAREER_ROLES.keys())
        )
        
    with gap_col2:
        # Fetch standard skills for this role
        role_skills = CAREER_ROLES[target_role_selected]
        
        # Auto-prepopulate some starting skills to show the app state in a loaded state,
        # but let the user select/unselect.
        default_acquired = role_skills[:len(role_skills)//3] if len(role_skills) > 2 else []
        
        # All unique skills in the dataset to allow custom skills
        all_dataset_skills = set()
        for s_list in df["Skills"].dropna():
            for s in s_list.split(","):
                all_dataset_skills.add(s.strip())
        
        # Combine role skills and all skills for list
        available_choices = sorted(list(set(role_skills).union(all_dataset_skills)))
        
        current_skills_selected = st.multiselect(
            "Select Skills You Already Possess:",
            options=available_choices,
            default=default_acquired,
            help="Select the skills you already have. The remaining skills required for the career role will define your skills gap."
        )
        
    st.markdown("---")
    
    # Run gap analysis
    analysis = recommender.analyze_skills_gap(current_skills_selected, target_role_selected)
    
    if analysis:
        # Progress Bar and Percentage
        prog_pct = analysis["progress_percentage"]
        st.markdown(f"#### 📈 Skills Readiness for **{target_role_selected}**")
        
        # Custom styled progress bar and status text
        progress_color = "#10b981" if prog_pct >= 70 else ("#f59e0b" if prog_pct >= 40 else "#ef4444")
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <span style="font-weight: 700; font-size: 16px; color: {progress_color};">{prog_pct}% Match Score</span>
            <span style="color: #9ca3af; font-size: 14px;">{len(analysis['acquired_skills'])} of {len(analysis['required_skills'])} Skills Acquired</span>
        </div>
        """, unsafe_allow_html=True)
        st.progress(prog_pct / 100.0)
        
        # Display side-by-side list of Acquired vs Missing
        lists_col1, lists_col2 = st.columns(2)
        
        with lists_col1:
            st.markdown("##### ✅ Acquired Skills")
            if len(analysis["acquired_skills"]) == 0:
                st.write("*No skills acquired yet. Pick some from the list above!*")
            else:
                for skill in analysis["acquired_skills"]:
                    st.markdown(f"""
                    <div class="gap-item-acquired">
                        <b>✔️ {skill}</b>
                    </div>
                    """, unsafe_allow_html=True)
                    
        with lists_col2:
            st.markdown("##### 🔍 Missing Skills (Your Gap)")
            if len(analysis["missing_skills"]) == 0:
                st.balloons()
                st.success("🎉 Incredible! You possess 100% of the skills required for this career path!")
            else:
                for skill in analysis["missing_skills"]:
                    st.markdown(f"""
                    <div class="gap-item">
                        <b>❌ {skill}</b>
                    </div>
                    """, unsafe_allow_html=True)
                    
        # Recommendation Learning Path Timeline
        if len(analysis["missing_skills"]) > 0:
            st.markdown("<br>---", unsafe_allow_html=True)
            st.markdown("### 🗺️ Tailored Learning Path to Bridge the Gap")
            st.write("Here is your structured course schedule to acquire your missing skills:")
            
            for i, skill in enumerate(analysis["missing_skills"], 1):
                course = analysis["recommendations"][skill]
                
                st.markdown(f"""
                <div style="display: flex; margin-bottom: 24px;">
                    <div style="margin-right: 20px; text-align: center; display: flex; flex-direction: column; align-items: center;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); display: flex; justify-content: center; align-items: center; font-weight: 700; color: #ffffff; font-size: 16px; box-shadow: 0 4px 10px rgba(99, 102, 241, 0.4);">
                            {i}
                        </div>
                        <div style="width: 2px; flex-grow: 1; background: rgba(255, 255, 255, 0.1); margin-top: 10px; min-height: 50px;"></div>
                    </div>
                    <div style="flex-grow: 1;">
                        <h4 style="margin-top: 0px; color: #a5b4fc; font-size: 18px; margin-bottom: 6px;">Focus Skill: <span style="color: #ffffff;">{skill}</span></h4>
                        <div style="margin-top: 10px;">
                            {render_course_card(course)}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.write("Select a career path above to begin your analysis.")
