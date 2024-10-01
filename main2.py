import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Crew
from tasks import MarketingAnalysisTasks
from agents import MarketingAnalysisAgents

# Load environment variables
load_dotenv()

# Initialize tasks and agents
tasks = MarketingAnalysisTasks()
agents = MarketingAnalysisAgents()

# Streamlit UI
st.title("Welcome to the Marketing Crew")

# Input fields
product_website = st.text_input("Enter the product website you want a marketing strategy for:")
product_details = st.text_input("Any extra details about the product or the Instagram post you want:")

# Check if the user has provided the necessary details
if product_website and product_details:
    
    # Create Agents
    product_competitor_agent = agents.product_competitor_agent()
    strategy_planner_agent = agents.strategy_planner_agent()
    creative_agent = agents.creative_content_creator_agent()

    # Create Tasks
    website_analysis = tasks.product_analysis(product_competitor_agent, product_website, product_details)
    market_analysis = tasks.competitor_analysis(product_competitor_agent, product_website, product_details)
    campaign_development = tasks.campaign_development(strategy_planner_agent, product_website, product_details)
    write_copy = tasks.instagram_ad_copy(creative_agent)

    # Create Crew responsible for Copy
    copy_crew = Crew(
        agents=[
            product_competitor_agent,
            strategy_planner_agent,
            creative_agent
        ],
        tasks=[
            website_analysis,
            market_analysis,
            campaign_development,
            write_copy
        ],
        verbose=True
    )

    # Run copy crew tasks
    ad_copy = copy_crew.kickoff()

    # Display ad copy
    st.subheader("Generated Instagram Ad Copy")
    st.write(ad_copy)

    # Create Agents for Image
    senior_photographer = agents.senior_photographer_agent()
    chief_creative_diretor = agents.chief_creative_diretor_agent()

    # Create Tasks for Image
    take_photo = tasks.take_photograph_task(senior_photographer, ad_copy, product_website, product_details)
    approve_photo = tasks.review_photo(chief_creative_diretor, product_website, product_details)

    # Create Crew responsible for Image
    image_crew = Crew(
        agents=[
            senior_photographer,
            chief_creative_diretor
        ],
        tasks=[
            take_photo,
            approve_photo
        ],
        verbose=True
    )

    # Run image crew tasks
    image = image_crew.kickoff()

    # Display image description
    st.subheader("Generated Image Description")
    st.write(image)

else:
    st.write("Please enter both the product website and product details to generate the marketing content.")
