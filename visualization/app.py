import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path


st.set_page_config(page_title="Tech Career Market Intelligence", layout="wide")

st.title("🚀 Tech Career Market Intelligence Dashboard")
st.write("Insights generated from real job market data")

# ---------- Helper to load JSON ----------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- Load Gold Data ----------
role_availability = load_json(Path("gold/role_availability.json"))
top_skills = load_json(Path("gold/top_skills_overall.json"))
skills_per_role = load_json(Path("gold/skills_per_role.json"))
top_locations = load_json(Path("gold/top_locations.json"))


# ---------- Role Availability ----------
st.header("📊 Top Job Roles (Top 10)")

roles_df = pd.DataFrame(role_availability, columns=["Role", "Jobs"])

# Sort and take top 10
roles_df = roles_df.sort_values(by="Jobs", ascending=False).head(10)

# Shorten long role names
roles_df["Role"] = roles_df["Role"].str.slice(0, 20) + "..."

st.bar_chart(
    roles_df.set_index("Role"),
    use_container_width=True
)


# ---------- Top Skills ----------
st.header("🛠️ Top Skills in Demand")

skills_df = pd.DataFrame(top_skills, columns=["Skill", "Count"])
st.bar_chart(skills_df.set_index("Skill"))


# ---------- Skills per Role ----------
st.header("🎯 Skills Required per Role")

selected_role = st.selectbox(
    "Select a Role",
    list(skills_per_role.keys())
)

role_skills = skills_per_role.get(selected_role, [])

if role_skills:
    role_df = pd.DataFrame(role_skills, columns=["Skill", "Count"])
    st.bar_chart(role_df.set_index("Skill"))
else:
    st.info("No skill data available for this role.")


# ---------- Locations ----------
st.header("📍 Top Hiring Locations")

locations_df = pd.DataFrame(top_locations, columns=["Location", "Count"])
st.bar_chart(locations_df.set_index("Location"))