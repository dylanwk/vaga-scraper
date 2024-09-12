from openai import OpenAI
import os


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def create_description(location_desc, title, amenities):
    chat_prompt = f"""You are a listing recommender. Given the title, location description, and amenities of a listing, provide an elegant ~50 word description of the space, highlighting unique and diverse aspects of the listing that make it special. In the description, emphasize the location and feel/aesthetic of the space. 

Respond ONLY with the description.

Listing title: {title}
Location description: {location_desc}
Amenities: {amenities}
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": chat_prompt,
            }
        ],
        model="gpt-3.5-turbo",
        temperature=0.7,
    )

    response_text = chat_completion.choices[0].message.content
    description = response_text.strip()
    

    return description