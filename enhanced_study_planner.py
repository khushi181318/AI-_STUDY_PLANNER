import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Ultimate AI Study Planner", layout="wide")

st.title("🧠 Ultimate AI Study Planner")

# ----------------------------
# Sidebar Inputs
# ----------------------------
st.sidebar.header("📌 Configure Your Study Plan")

subjects_input = st.sidebar.text_area(
    "Enter subjects, priority (1=high), and estimated study hours/week (comma separated)", 
    "Math,1,8\nPhysics,2,6\nAI,1,5\nC++,2,4\nEnglish,3,3"
)

weak_areas_input = st.sidebar.text_area(
    "Enter weak areas/topics (comma separated)", 
    "Math: Calculus, AI: Machine Learning"
)

prerequisites_input = st.sidebar.text_area(
    "Enter prerequisites/topics for subjects (comma separated)", 
    "AI: Python, Math: Algebra, C++: Basic Programming"
)

daily_hours = st.sidebar.slider("Available study hours per day", min_value=1, max_value=12, value=6)

# ----------------------------
# Parse Inputs
# ----------------------------
subjects = []
for line in subjects_input.split("\n"):
    parts = line.split(",")
    if len(parts) == 3:
        name, priority, hours = parts
        subjects.append({
            "name": name.strip(),
            "priority": int(priority.strip()),
            "hours": int(hours.strip())
        })

weak_areas = {}
for entry in weak_areas_input.split(","):
    if ":" in entry:
        subj, topic = entry.split(":")
        weak_areas[subj.strip()] = topic.strip()

prerequisites = {}
for entry in prerequisites_input.split(","):
    if ":" in entry:
        subj, topic = entry.split(":")
        prerequisites[subj.strip()] = topic.strip()

# ----------------------------
# Weekly Planner
# ----------------------------
days = ["Saturday","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday"]

def generate_weekly_plan(subjects, daily_hours):
    subjects_sorted = sorted(subjects, key=lambda x: x['priority'])
    plan = {day: [] for day in days}
    day_index = 0

    for subj in subjects_sorted:
        hours_left = subj['hours']
        while hours_left > 0:
            hours_today = min(daily_hours, hours_left)
            task_str = f"{subj['name']} ({hours_today} hrs)"
            # Add weak area suggestion if exists
            if subj['name'] in weak_areas:
                task_str += f" - Focus on {weak_areas[subj['name']]}"
            # Add prerequisite reminder if exists
            if subj['name'] in prerequisites:
                task_str += f" [Prerequisite: {prerequisites[subj['name']]}]"
            plan[days[day_index % 7]].append(task_str)
            hours_left -= daily_hours
            day_index += 1

    # Fill empty days
    for day in days:
        if not plan[day]:
            plan[day].append("Check pending tasks or review weak areas")

    return plan

weekly_plan = generate_weekly_plan(subjects, daily_hours)

# ----------------------------
# Display Weekly Plan
# ----------------------------
st.subheader("📅 Weekly Study Schedule")
for day, tasks in weekly_plan.items():
    st.write(f"**{day}**")
    for t in tasks:
        st.write(f"- {t}")

# ----------------------------
# Visual: Weekly Study Hours
# ----------------------------
st.subheader("📊 Study Hours Distribution")
data = []
for day, tasks in weekly_plan.items():
    for t in tasks:
        if "(" in t:
            name_hours = t.split("(")
            subj_name = name_hours[0].strip()
            hrs = int(name_hours[1].split()[0])
            data.append({"Day": day, "Subject": subj_name, "Hours": hrs})

df_hours = pd.DataFrame(data)

chart = alt.Chart(df_hours).mark_bar().encode(
    x='Day',
    y='Hours',
    color='Subject',
    tooltip=['Day','Subject','Hours']
).properties(width=700, height=400)

st.altair_chart(chart, use_container_width=True)

# ----------------------------
# Weak Areas Highlight
# ----------------------------
if weak_areas:
    st.subheader("⚠️ Weak Areas / Focus Topics")
    for subj, topic in weak_areas.items():
        st.write(f"- {subj}: {topic}")

# ----------------------------
# Detailed Daily Timetable
# ----------------------------
st.subheader("🗓 Detailed Daily Timetable")
selected_day = st.selectbox("Select a day", days)

if selected_day in weekly_plan:
    st.write(f"### {selected_day} Timetable")
    for task in weekly_plan[selected_day]:
        st.write(f"- {task}")

st.success("✅ Planner ready! Update sidebar to regenerate dynamically.")
