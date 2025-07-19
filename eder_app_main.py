
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="עדר - ניהול עדר חכם", layout="centered")
st.title("🐂 עדר - עוזר הבקר שלך")

# --- טעינת נתוני הדמו ---
@st.cache_data
def load_data():
    data = pd.DataFrame({
        "מספר": [201, 202, 203, 204, 208, 216, 217],
        "סוג": ["פרה"]*7,
        "תאריך המלטה אחרון": [
            "2023-07-01", "2022-12-15", "2023-04-03", "2024-02-20", "2024-07-01", "2023-06-10", "2023-01-05"
        ],
        "גיל": [5.5, 4.8, 3.2, 6.1, 4.0, 2.5, 3.8],
        "סטטוס": ["פעילה"]*7
    })
    data["תאריך המלטה אחרון"] = pd.to_datetime(data["תאריך המלטה אחרון"])
    return data

animals = load_data()

# --- תצוגה ודיווח ---
st.subheader("🔎 בירור על פרה")
cow_id = st.text_input("הזן מספר פרה")

if cow_id:
    try:
        cow_id_int = int(cow_id)
        cow = animals[animals["מספר"] == cow_id_int]
        if not cow.empty:
            st.success(f"פרה {cow_id} נמצאה:")
            st.dataframe(cow)
            delta = datetime.now() - cow["תאריך המלטה אחרון"].values[0]
            if delta.days >= 330:
                st.warning(f"⚠️ פרה {cow_id} אמורה להמליט בקרוב! עברו {delta.days} ימים מהמלטה האחרונה.")
        else:
            st.error("לא נמצאה פרה במספר הזה.")
    except:
        st.error("מספר לא תקין.")

st.divider()

st.subheader("📝 דיווח על המלטה חדשה")
cow_birth_id = st.text_input("איזו פרה המליטה עכשיו?")
if st.button("דווח המלטה"):
    try:
        cow_birth_id_int = int(cow_birth_id)
        index = animals[animals["מספר"] == cow_birth_id_int].index
        if not index.empty:
            animals.loc[index, "תאריך המלטה אחרון"] = pd.to_datetime(datetime.now())
            st.success(f"עודכן תאריך המלטה של פרה {cow_birth_id} להיום.")
        else:
            st.error("הפרה לא קיימת ברשימה.")
    except:
        st.error("מספר לא תקין.")
