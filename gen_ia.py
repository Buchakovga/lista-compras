import os
from google import genai
from google.genai import types


def generate(prompt,img,mime_type):
    
    client = genai.Client(
     
    )

    tools = [
        {
            'type': 'google_search',
        },
    ]

    generation_config = {
        'temperature': 1,
        'max_output_tokens': 65536,
        'top_p': 0.95,
        'thinking_level': 'high',
    }


    interaction = client.interactions.create(
        model='models/gemini-3-flash-preview',
        input=[
            {
                'type': 'text',
                'text': prompt,
            }
            # ,
            # {
            #     'type': 'image/png',
            #     'data': img,
            #     'mime_type': type,
            # },
        ],
        tools=tools,
        generation_config=generation_config,
    )

    print(interaction.steps[-1])


if __name__ == "__main__":
    generate()
