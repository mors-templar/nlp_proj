import streamlit as st
import pandas as pd
import plotly.express as px
import time
import database as db
import sentiment_model as sentiment

st.set_page_config(
    page_title="User Feedback Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    db.create_database()
except Exception as e:
    st.error(f"Error initializing the database: {e}")
    st.stop()


# Main Application with Tabs 

tab1, tab2, tab3 = st.tabs(["Input Form", "Analytics Dashboard", "Raw Data"])

with tab1:
    st.title("NLP Prototype - Feedback Form")
    st.write("Submit your feedback below and see the sentiment analysis in action.")

    user_text = st.text_area("Your Feedback", height=150)
    submit_button = st.button("Submit")

    if submit_button and user_text:
        try:
            score, label = sentiment.get_user_sentiment(user_text)

            db.insert_feedback(user_text, score, label)
            
            st.success(f"Feedback submitted! Sentiment: **{label}** (Score: {score:.2f})")
                            
            # Rerun with a delay to showcase result and to update the dashboard immediately
            time.sleep(5)            
            st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {e}")

with tab2:
    st.title("User Feedback Dashboard")
    st.write("This section shows real-time analytics of all submitted feedback.")

    try:
        # Fetch all feedback data from the database for dashboard and raw tabs
        all_feedback = db.get_all_feedback()
        
        if not all_feedback:
            st.info("No feedback submitted yet. Be the first to add some!")
        else:
            df = pd.DataFrame(all_feedback, columns=['id', 'text', 'sentiment_score', 'sentiment_label', 'timestamp'])
            
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Total Feedback", value=len(df))
            with col2:
                positive_count = df[df['sentiment_label'] == 'Positive'].shape[0]
                st.metric(label="Positive Feedback", value=positive_count)

            # Create and display visualizations (pie char and bar chart)
            st.markdown("### Sentiment Distribution")
            sentiment_counts = df['sentiment_label'].value_counts().reset_index()
            fig = px.pie(
                sentiment_counts,
                values='count',
                names='sentiment_label',
                title='Sentiment Breakdown'
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Feedback Over Time")
            time_df = df.groupby(df['timestamp'].dt.date)['sentiment_label'].value_counts().unstack(fill_value=0)
            st.bar_chart(time_df)

    except Exception as e:
        st.error(f"Error loading dashboard: {e}")


with tab3:
    st.title("Raw Feedback Data")
    st.write("Below is a table of all the raw data stored in the database.")
    
    try:
        all_feedback_raw = db.get_all_feedback()
        if all_feedback_raw:
            df_raw = pd.DataFrame(all_feedback_raw)
            st.dataframe(df_raw)
        else:
            st.info("No raw data to display.")
    except Exception as e:
        st.error(f"Error loading raw data: {e}")
