from collections import deque
from typing import List
from datetime import datetime, UTC

from ...crud.learning_path_content import get_learning_path_content
from ...models.learning_path_content import LearningPathContent, ChatMessage
from ...models.user_concept_mastery import UserConceptMastery, Concept
from ..generative_ai import openai_service

import os
import configparser

from langchain.memory import ConversationSummaryMemory
from langchain_openai import OpenAI

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../../config.ini'))

openai_api_key = config['openai']['OPENAI_API_KEY']
model = config['openai']['MODEL']

llm = OpenAI(api_key=openai_api_key, 
                model=model,
                temperature=0.3)


class AITutor:
    def __init__(self,learning_path_content: LearningPathContent, user_concept_mastery: UserConceptMastery):
        self.topic_name = learning_path_content.title
        self.current_level = learning_path_content.levels[learning_path_content.current_level_index]
        self.current_learning_objective = self.current_level.learning_objectives[learning_path_content.current_learning_objective_index]

        self.recent_messages = deque(learning_path_content.chat_history[-10:])

        self.learning_objective_memory = ConversationSummaryMemory(llm=llm,
                                                max_token_limit=500,
                                                buffer=self.learning_objective_summary)

        self.level_memory = ConversationSummaryMemory(llm=llm,
                                                max_token_limit=500,
                                                buffer=self.level_chat_summary)
        
        self.learning_path_memory = ConversationSummaryMemory(llm=llm,
                                                max_token_limit=500,
                                                buffer=self.chat_summary)
        
        self.user_concept_mastery = user_concept_mastery
        
    def receive_message(self,user_message: ChatMessage):
        self.recent_messages.popleft()
        self.recent_messages.append(user_message)
        evaluation = self.evaluate_response(user_message)

    async def evaluate_response(self, user_message: ChatMessage):
        evaluation_response = openai_service.response_evaluator(
            prior_exchanges=list(self.recent_messages),
            conversation_history_summary=self.learning_path_memory.moving_summary_buffer,
            mastery_scores=self.mastery_scores,
            topic=self.topic_name,
            learning_objective=self.current_learning_objective.objective_text
        )

        existing_concepts_dict = {concept.concept_name: concept for concept in self.user_concept_mastery.concepts}

        for concept_name in evaluation_response['new_concepts']:
            if concept_name not in existing_concepts_dict:
                new_concept= Concept(
                concept_name=concept_name,
                mastery_score=0.38,
                last_updated=datetime.now(UTC)
                )
                
                self.user_concept_mastery.concepts.append(new_concept)
                existing_concepts_dict[concept_name] = new_concept
        
        for concept_name, mastery_evaluation in evaluation_response['concept_mastery_evaluation'].items():
            if concept_name in existing_concepts_dict:
                existing_concept = existing_concepts_dict[concept_name]
                existing_concept.mastery_score = adjust_mastery_from_feedback(existing_concept.mastery_score,mastery_evaluation)

    def exchange_message(self, user_message: ChatMessage):
        
        
        
