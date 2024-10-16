from openai import OpenAI
import os
import configparser
from ..crud import prompt
from ..database import init_postgres

from sqlalchemy.orm import Session

# Load configuration
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../config.ini'))

openai_api_key = config['openai']['OPENAI_API_KEY']
model = config['openai']['MODEL']

client = OpenAI(api_key=openai_api_key)

def generate_learning_path(topic: str, experience: str) -> str:
    db_gen = init_postgres()
    db = next(db_gen)

    prompt_name = "Learning Path Generation"
    current_prompt = prompt.get_prompt_by_name(db=db,name=prompt_name)

    if not current_prompt:
      raise ValueError(f"No prompt found for {prompt_name}")
    
    user_content_template = current_prompt.user_content
    user_content = user_content_template.format(topic=topic, experience=experience)
    
    openai_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": current_prompt.system_content}, 
             {"role": "user", "content": user_content}
        ],
        temperature= current_prompt.temperature
    )

    output = openai_response.choices[0].message

    db_gen.close()

    return output

def regenerate_learning_path(prior_content: str, topic: str, experience: str, feedback: str) -> str:
    db_gen = init_postgres()
    db = next(db_gen)

    prompt_name = "Learning Path Regeneration"
    regenerate_content_prompt = prompt.get_prompt_by_name(db=db,name="Learning Path Regeneration")

    if not regenerate_content_prompt:
       raise ValueError(f"No prompt found for {prompt_name}")
    
    user_content_template = regenerate_content_prompt.user_content
    user_content = user_content_template.format(prior_content=prior_content, topic=topic, experience=experience, feedback=feedback)

    openai_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": regenerate_content_prompt.system_content}, 
             {"role": "user", "content": user_content}
        ],
        temperature= regenerate_content_prompt.temperature
    )

    output = openai_response.choices[0].message

    db_gen.close()

    return output
    


