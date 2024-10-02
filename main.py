from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from textwrap import dedent
from crewai import Crew

from agents import MarketingAnalysisAgents
from tasks import MarketingAnalysisTasks

tasks = MarketingAnalysisTasks()
agents = MarketingAnalysisAgents()

st.header("Welcome to the marketing Crew") 
product_website = st.text_input("What is the product website you want a marketing strategy for?")
product_details = st.text_input("Any extra details about the product and or the instagram post you want?")


# print("## Welcome to the marketing Crew")
# print('-------------------------------')
#product_website = input("What is the product website you want a marketing strategy for?\n")
#product_details = input("Any extra details about the product and or the instagram post you want?\n")

if product_website and product_details:
    
       # Criando Agentes
		product_competitor_agent = agents.product_competitor_agent()
		strategy_planner_agent = agents.strategy_planner_agent()
		creative_agent = agents.creative_content_creator_agent()


		# Criando Tarefas
		website_analysis = tasks.product_analysis(product_competitor_agent, product_website, product_details)
		market_analysis = tasks.competitor_analysis(product_competitor_agent, product_website, product_details)
		campaign_development = tasks.campaign_development(strategy_planner_agent, product_website, product_details)
		write_copy = tasks.instagram_ad_copy(creative_agent)

		# Create Crew responsible for Copy -- Criando a tripulação responsável pelo Cópia
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

		ad_copy = copy_crew.kickoff()

		# Create Crew responsible for Image
		senior_photographer = agents.senior_photographer_agent()
		chief_creative_diretor = agents.chief_creative_diretor_agent()

		# Create Tasks for Image
		take_photo = tasks.take_photograph_task(senior_photographer, ad_copy, product_website, product_details)
		approve_photo = tasks.review_photo(chief_creative_diretor, product_website, product_details)

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

		image = image_crew.kickoff()
	

		# Print results
		print("\n\n########################")
		print("## Here is the result")
		print("########################\n")
		print("Your post copy:")
		print(ad_copy)
		print("'\n\nYour midjourney description:")
		print(image)

else:
	st.write("Please enter both the product website and product details to generate the marketing content.")

