import json
import os
import requests
from langchain.tools import tool
from langchain_openai import ChatOpenAI

class BrowserTools:
    @tool("Scrape website content")
    def scrape_and_summarize_website(self, website):
        """Scrapes and summarizes website content using the Serper API and OpenAI."""
        # Prepare the Serper API request
        url = "https://google.serper.dev/search/content"
        payload = json.dumps({"url": website})
        headers = {
            'Authorization': f"Bearer {os.environ['SERPER_API_KEY']}",
            'Content-Type': 'application/json'
        }

        # Make the request to Serper API
        response = requests.post(url, headers=headers, data=payload)

        # Extract and partition HTML content
        if response.status_code == 200:
            content = response.json().get('content', '')
        else:
            raise Exception(f"Failed to retrieve content: {response.status_code} {response.text}")

        # Split content into manageable chunks
        content_chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []

        # Process each chunk with the LLM (OpenAI)
        chat_model = ChatOpenAI(model=os.environ['MODEL'])
        for chunk in content_chunks:
            # Create the task description
            task_description = (
                f"Analyze and summarize the content below, including all relevant information. "
                f"Return only the summary.\n\nCONTENT\n----------\n{chunk}"
            )

            # Generate summary with the LLM
            summary = chat_model.run(task_description)
            summaries.append(summary)

        # Combine all summaries into one
        final_summary = "\n\n".join(summaries)
        return final_summary
