import os
import json
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from .website import Website

load_dotenv()

MODEL = 'gpt-4o-mini'  # Specify the OpenAI model to use
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')  # Get API key from environment or use default

# Initialize OpenAI client with the API key
openai = OpenAI(api_key=OPENAI_API_KEY)

class LinkAnalyzer:
    """
    A class to analyze and categorize links from a website.
    """
    # System prompt for the OpenAI model to categorize links
    LINK_SYSTEM_PROMPT = """
    You are provided with a list of links found on a webpage. Your task is to first categorize each link into one of the following categories:
    - about page
    - careers page
    - terms of service
    - privacy policy
    - contact page
    - other (please specify).

    Once the links are categorized, please choose which links are most relevant to include in a brochure about the company. 
    The brochure should only include links such as About pages, Careers pages, or Company Overview pages. Exclude any links related to Terms of Service, Privacy Policy, or email addresses.

    Respond in the following JSON format:
    {
        "categorized_links": [
            {"category": "about page", "url": "https://full.url/about"},
            {"category": "careers page", "url": "https://full.url/careers"},
            {"category": "terms of service", "url": "https://full.url/terms"},
            {"category": "privacy policy", "url": "https://full.url/privacy"},
            {"category": "other", "specify": "contact page", "url": "https://full.url/contact"}
        ],
        "brochure_links": [
            {"type": "about page", "url": "https://full.url/about"},
            {"type": "careers page", "url": "https://full.url/careers"}
        ]
    }

    Please find the links below and proceed with the task:

    Links (some may be relative links):
    [INSERT LINK LIST HERE]
    """

    @staticmethod
    def get_links(website: Website) -> Dict:
        """
        Analyze and categorize links from a given website.
        
        :param website: A Website object containing the links to analyze
        :return: A dictionary containing categorized links and brochure-relevant links
        """
        # Prepare the user prompt for the OpenAI model
        user_prompt = f"Here is the list of links on the website of {website.url} - "
        user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
    Do not include Terms of Service, Privacy, email links.\n"
        user_prompt += "Links (some might be relative links):\n"
        user_prompt += "\n".join(website.links)

        # Make an API call to OpenAI for link analysis
        completion = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": LinkAnalyzer.LINK_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
