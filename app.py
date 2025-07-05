import streamlit as st
import requests
from st_keyup import st_keyup

API_KEY = ""
BASE_URL = "https://api.spoonacular.com"

if "ingredients" not in st.session_state:
    st.session_state.ingredients = []

if "chosen_meals" not in st.session_state:
    st.session_state.chosen_meals = {}

if "recipes" not in st.session_state:
    st.session_state.recipes = {}

# Sidebar content (was col1)
with st.sidebar:
    st.subheader("Your Ingredients:")

    query = st_keyup("Start typing an ingredient...")

    suggestions = []
    if query:
        res = requests.get(
            f"{BASE_URL}/food/ingredients/autocomplete",
            params={"query": query, "number": 5, "apiKey": API_KEY}
        )
        if res.ok:
            suggestions = [item["name"] for item in res.json()]
            
        if suggestions:
            selected = st.selectbox("Choose from suggestions:", suggestions, key="ingredient_select")
            if st.button("Add", key="add_ingredient"):
                if selected not in st.session_state.ingredients:
                    st.session_state.ingredients.append(selected)
        else:
            if query:
                st.info("No suggestions found.")

    # Show current list
    if st.session_state.ingredients:
        badges = " ".join([f":blue-badge[{ingredient}]" for ingredient in st.session_state.ingredients])
        st.markdown(badges)

        if st.button("Clear all"):
            st.session_state.ingredients = []

# Main content
st.subheader("Meal Plan:", divider=True)

mon, tue, wed, thu, fri, sat, sun = st.columns(7)

with mon:
    with st.container():
        st.markdown("**Monday**")
        st.image("https://spoonacular.com/recipeImages/716429-556x370.jpg")
        st.write("Pasta Carbonara")
with tue:
    with st.container():
        st.markdown("**Tuesday**")
        st.image("https://spoonacular.com/recipeImages/716429-556x370.jpg")
        st.write("Pasta Carbonara")
with wed:
    with st.container():
        st.markdown("**Wednesday**")
        st.image("https://spoonacular.com/recipeImages/716429-556x370.jpg")
        st.write("Pasta Carbonara")
with thu:
    with st.container():
        st.markdown("**Thursday**")
        st.image("https://spoonacular.com/recipeImages/716429-556x370.jpg")
        st.write("Pasta Carbonara")
with fri:
    with st.container():
        st.markdown("**Friday**")
        st.image("https://spoonacular.com/recipeImages/716429-556x370.jpg")
        st.write("Pasta Carbonara")
with sat:
    with st.container():
        st.markdown("**Saturday**")
        st.image("https://spoonacular.com/recipeImages/716429-556x370.jpg")
        st.write("Pasta Carbonara")
with sun:
    with st.container():
        st.markdown("**Sunday**")
        st.image("https://spoonacular.com/recipeImages/716429-556x370.jpg")
        st.write("Pasta Carbonara")

def get_recipes_by_ingredients(ingredients_list):
    query_string = ",".join(ingredients_list)
    res = requests.get(
        f"{BASE_URL}/recipes/findByIngredients",
        params={
            "ingredients": query_string,
            "number": 20,  # You can increase this
            "ranking": 1,
            "apiKey": API_KEY
        }
    )
    if res.ok:
        return res.json()
    else:
        st.error("Failed to fetch recipes.")
        return []

if st.session_state.ingredients:
    st.subheader("Recipes You Can Make:")
    recipes = get_recipes_by_ingredients(st.session_state.ingredients)

    cols = st.columns(3)
    for i, recipe in enumerate(recipes):
        with cols[i % 3]:
            st.markdown(f"""
                <div style="border:1px solid #ccc; border-radius:10px; padding:10px; margin-bottom:10px;">
                    <h4>{recipe['title']}</h4>
                    <img src="{recipe['image']}" width="100%" style="border-radius:8px;" />
                    <p><b>Used Ingredients:</b> {len(recipe['usedIngredients'])} | 
                       <b>Missing:</b> {len(recipe['missedIngredients'])}</p>
                    <a href="https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']}" 
                       target="_blank">🔗 View Recipe</a>
                </div>
            """, unsafe_allow_html=True)