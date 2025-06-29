import streamlit as st
from openai import OpenAI
import pandas as pd
import json

# ==== CONFIGURE OPENAI API ====

client = OpenAI(api_key="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")


# ==== LOAD DATASET ====
df = pd.read_csv("netflix_titles.csv")
df_cleaned = df[['title', 'type', 'listed_in', 'description']].dropna()
df_cleaned.rename(columns={'listed_in': 'genres'}, inplace=True)
df_sample = df_cleaned.sample(50, random_state=42).to_dict(orient="records")

# ==== STREAMLIT UI ====
st.set_page_config(page_title="Netflix Recommender", layout="wide")
st.title("🎬 Netflix-style Movie/TV Show Recommender")

st.markdown("Enter your preferences to get smart recommendations.")

user_titles = st.text_area("📺 Shows/Movies you love")
user_genres = st.multiselect("🎭 Preferred Genres", ["Drama", "Comedy", "Action", "Romance", "Thriller", "Documentary", "Sci-Fi", "Fantasy", "Horror", "Crime"])
user_mood = st.selectbox("🧠 Current Mood", ["Light-hearted", "Adventurous", "Romantic", "Dark", "Thoughtful","Mind-Bending","Chill","Emotional"])
user_type = st.selectbox("Type",["Movies","TV Shows","Movies and TV Shows"])
if st.button("🔍 Get Recommendations"):
    with st.spinner("Talking to GPT-4..."):
        prompt = f"""
You are a Netflix movie and TV show expert.

A user enjoys these shows: {user_titles}
Preferred genres: {', '.join(user_genres)}
Current mood: {user_mood}

Below is a dataset of Netflix content:
{json.dumps(df_sample, indent=2)}

Based on the user preferences and dataset, recommend 5 {user_type} with short explanations.
Return JSON like:
[
  {{"title": "...", "reason": "..."}},
  ...
]
"""

        response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.8
)


        try:
            recommendations = json.loads(response.choices[0].message.content)

            st.subheader("📢 Recommendations")
            for rec in recommendations:
                st.markdown(f"**🎬 {rec['title']}**")
                st.write(f"📝 {rec['reason']}")
        except Exception as e:
            st.error("Could not parse GPT response. Check API output.")
            st.text(response.choices[0].message['content'])
