from openai import OpenAI
import os
import configparser
import json

from sqlalchemy.orm import Session

from .prompt_response_models import DiagnosticTestResponse, ContentValidatorResponse, LearningPathGeneratorResponse, DiagnosticTestResultResponse, AITutorResponseOutput, ResponseEvaluatorOutput

# Load configuration
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../../config.ini'))

openai_api_key = config['openai']['OPENAI_API_KEY']
model = config['openai']['MODEL']

client = OpenAI(api_key=openai_api_key)

def generate_learning_path_content(topic):
    learning_path_generator_response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": '''
    You are an educational assistant designed to create personalized learning paths for students. 
    After completing this learning path, students should be able to confidently answer any 
    questions related to the topic during a technical interview. They should also be able to apply the concept to 
    solve problems involving those topics in the context of a technical interview.

    You will be provided with:
    - The user's requested topic

    Instructions:
    - Look at the topic requested by the user. Think of the concepts needed to master the topic, 
            especially in the context of a technical interview. 
    - Enclose your thought process and analysis in "generation working": """ """.
    - Using the identified concepts, create an ordered list of levels, arranging them in increasing difficulty.
        - If a concept has prerequisites, place those prerequisites first.
        - At the end of the analysis, describe why you chose the specific order.
    - For each concept (level), generate a list of granular learning objectives.
    - Review the concepts and learning objectives you have outlined, and streamline them by 
    removing any duplicate objectives. Ensure that the learning path is concise and designed to avoid repeating the same content, 
    so users can progress efficiently without covering the same material twice. Enclose your thought process and any changes made in "generation working".
    - Format the output as:
    """
    "output": 
    {
        "levels": {
                    "concept_name": "<Concept Name>",
                        "learning_objectives": [
                        {"objective_text": "<Learning Objective 1>"},
                        {"objective_text": "<Learning Objective 2>"},
                        ...
                        ]     
                }    ,
        "generation_working": "<Working>"                 
    }      
             
    An example output is provided:
    "output": 
    {
        "levels": {
            {
                "concept_name": "Basic Understanding of Heaps",
                "learning_objectives": [
                    {"objective_text": "Define what a heap is and describe its properties."},
                    {"objective_text": "Differentiate between Min-Heap and Max-Heap."},
                    {"objective_text": "Explain the differences between a heap and a binary search tree."}
                ]
            },
            {
                "concept_name": "Heap Operations",
                "learning_objectives": [
                    {"objective_text": "Demonstrate how to insert an element into a heap while maintaining heap properties."},
                    {"objective_text": "Explain and perform the deletion of the root element in a heap."},
                    {"objective_text": "Access the root element using the peek operation without removing it."}
                ]
            }             
        },
        "generation_working": "Your thought process and analysis here"        
    }
    """
    '''
                }, 
                {"role": "user",
                "content": f'''
                Topic: {topic}
                '''}
        ],
        response_format=LearningPathGeneratorResponse,
        temperature= 0.5
    )

    learning_path_generator_response_output = json.loads(learning_path_generator_response.choices[0].message.content)

    return learning_path_generator_response_output
    
def validate_learning_path_content(topic,learning_path):
    learning_path_validator_response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": '''
    You are an experienced technical interviewer tasked with evaluating an educational assistant’s proposed learning path and objectives for a particular topic.

    You will be provided with:
    - The user's requested topic
    - Learning path for topic, with levels each containing one concept that comprises of multiple learning objectives

    Instructions:
    - Look at the topic that the user has provided. Think of how you would evaluate a student's proficiency
            in that topic during a technical interview. Enclose your working in "analysis".
    - Look at the learning path and objectives suggested by the educational assistant. Compare it with what
            you have come up with in the previous step. Evaluate whether there are any aspects that the educational assistant
            has missed out on or should be taught in more rigor, and whether there are any aspects which you feel are not sufficient. 
            Enclose your thoughts and reasoning at the back of the previously generated "analysis".
    - Based on your evaluation, decide if the educational assistant has to make any change. If yes, craft feedback in a way such that the educational
            assistant will be able to understand what changes he has to make. If no, the feedback should be 'no changes needed'. Enclose this in "feedback".
    '''
                }, 
                {"role": "user",
                "content": f'''
                Topic: {topic}
                Learning Objectives: {learning_path}
                '''}
        ],
        response_format=ContentValidatorResponse,
        temperature= 0.5
    )

    learning_path_validator_response_output = json.loads(learning_path_validator_response.choices[0].message.content)
    
    return learning_path_validator_response_output

def modify_learning_path_content(topic, learning_path, feedback):
    learning_path_modifier_response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": '''
    You are an educational assistant designed to create personalized learning paths for students. 
    After completing this learning path, students should be able to confidently answer any 
    questions related to the topic during a technical interview. They should also be able to apply the concept to 
    solve problems involving those topics in the context of a technical interview. You are tasked with updating a learning path
    based on provided feedback.

    You will be provided with:
    - The user's requested topic
    - An existing learning path with structured concepts and objectives
    - Feedback to improve or adjust this learning path based on technical interview requirements

    Instructions:
    - Review the feedback provided. Think of how you can use the feedback to improve or adjust the learning path. 
            Enclose your thought process in "generation_working".
    - Update the learning path, making necessary adjustments to concepts or objectives based on the feedback.
    - Format the output as:
    """
    "output": 
    {
        "levels": [{
                    "concept_name": "<Concept Name>",
                        "learning_objectives": [
                        {"objective_text": "<Learning Objective 1>"},
                        {"objective_text": "<Learning Objective 2>"},
                        ...
                        ]     
                }],
        "generation_working": "<Working>"                 
    }      
             
    An example output is provided:
    "output": 
    {
        "levels": [
            {
                "concept_name": "Basic Understanding of Heaps",
                "learning_objectives": [
                    {"objective_text": "Define what a heap is and describe its properties."},
                    {"objective_text": "Differentiate between Min-Heap and Max-Heap."},
                    {"objective_text": "Explain the differences between a heap and a binary search tree."}
                ]
            },
            {
                "concept_name": "Heap Operations",
                "learning_objectives": [
                    {"objective_text": "Demonstrate how to insert an element into a heap while maintaining heap properties."},
                    {"objective_text": "Explain and perform the deletion of the root element in a heap."},
                    {"objective_text": "Access the root element using the peek operation without removing it."}
                ]
            }             
        ],
        "generation_working": "Your thought process and analysis here"        
    }
    """
    '''
                }, 
                {"role": "user",
                "content": f'''
                Topic: {topic}
                Existing Learning Path: {learning_path}
                Feedback: {feedback}
                '''}
        ],
        response_format=LearningPathGeneratorResponse,
        temperature= 0.3
    )

    learning_path_modifier_response_output = json.loads(learning_path_modifier_response.choices[0].message.content)

    return learning_path_modifier_response_output

def generate_diagnostic_test(topic, learning_path):
    diagnostic_test_generator_response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": '''
    You are an educational tutor tasked with training students for technical interviews. 
    A user has requested your help with a specific topic, and you have developed a structured learning path with concepts and objectives.
    You now want to evaluate the student's proficiency in the topic using a diagnostic test.

    You will be provided with:
    - The user's requested topic
    - A structured learning path with concepts and learning objectives

    Instructions:
    1. Generate Diagnostics Questions:
        - Review the learning objectives and concepts.
        - Create questions that assess the practical understanding of these concepts, covering as many learning objectives as possible.
        - Design questions that evaluate multiple learning objectives whenever possible.
        - Choose the most appropriate question type for each learning objective, considering what will effectively assess the student's understanding. Possible
             question types include:
              - Multiple Choice Questions (MCQs)
              - Fill-in-the-blanks
              - Coding Problems - unless explicitly specified, make this language agnostic
              - Open-Ended Questions
              - Case Studies or Scenarios
          - Ensure that all questions are fully self-contained, providing any necessary data, schemas, code snippets, or context required for the student to answer. For coding questions, 
              provide users with a 'example_input' and 'example_output' under 'provided_data_schemas' so they can understand the question better and check if their output is correct.
          - Make sure users have all the information they need to solve this question. Give context to help them better understand the problem.
          - Tag each question with the learning objectives it assesses.
          - Enclose the questions you have come up with in """ """ and add it into "working".
    2. Estimate Time for Each Question:
        - Assign an estimated completion time to each question.
        - Calculate the total estimated time for the diagnostic test.
        - If the total time exceeds 60 minutes, do the following such that the test strictly takes less than 60 minutes:
            -  Identify questions which can be replaced with simpler alternatives to reduce the total time while still effectively assessing the mastery of concepts.
            - Prioritize questions that cover multiple learning objectives, and questions that cover key objectives.
        - Update "working" with your thought process, adjustments made to ensure the test remains under 60 minutes, and the updated diagnostic test.
    3. Prepare Output Format for Each Question:
        - For each question, provide the following in a database-friendly format:
            1. Question: The text of the question
            2. Provided Data/Schemas: If applicable
            3. Learning Objectives Evaluated: A list of learning objectives the questions assesses
            4. Estimated Time: Time allocated for the question
            5. Difficulty: Based on the following factors, assign a difficulty level to this question:

            - Conceptual Complexity: Rate from 1 (basic) to 5 (complex) based on the depth of understanding required.
            - Solution Steps: Rate from 1 (few steps) to 5 (many steps) based on the number of logical stages in problem-solving.
            - Familiarity Requirement: Rate from 1 (minimal prior knowledge) to 5 (advanced knowledge required).
            - Ambiguity Level: Rate from 1 (clear question) to 5 (requires high interpretation).
            - Solution Optimization: Rate from 1 (basic solution acceptable) to 5 (requires optimal solution).
                
            Use these scores to classify the question as:
            - Beginner: Total score 5-10
            - Intermediate: Total score 11-18
            - Advanced: Total score 19+
            
            6. Scoring Rubrics: Tailor the rubrics to each question by specifying clear evaluation criteria based on the learning objectives and question type. For each criterion, include:
                - Description: A brief explanation of what is being assessed.
                - Max Score: The maximum points allocated for this criterion.
            - Evaluation Criteria: Evaluate response based on following criteria:
                - Understanding: Assess conceptual clarity and comprehension (30%)
                - Application: Evaluate the ability to apply concepts to solve problems (25%)
                - Analysis: Assess the ability to break down complex problems and identify components (15%)
]                 - Efficiency: For solution-based questions, evaluate optimality and resource utilization (15%)
                - Accuracy: Check for correctness in solutions, calculations, or reasoning (15%)
            If a criterion does not apply to this question (e.g., Efficiency for purely theoretical responses), restribute its weight among the
            remaining criteria proportionally. Assign a max score for each question based on this proportion, with the maximum cumulative sum being 10.
            Ensure that the sum of maximum scores for all criteria must be equal to 10. 
            7. Total Max Score: The sum of maximum scores for all criteria in the question.
            8. Answer: The model answer or solution.
        
    4. Prepare Final Output Summary:
        - Include a final_evaluation field summarizing the changes you have made, and your reasoning process. Also include the total estimated time and any adjustments made to ensure the test remains under 60 minutes.

    Output Format Example:
    """
{
  "questions": [
    {
      "question": "Implement a function that finds the maximum sum of any contiguous subarray of size `k` within a given array of integers.",
      "provided_data_schemas": {
        "example_input": """
          "arr": [2, 1, 5, 1, 3, 2],
          "k": 3
        """
        ,
        "example_output": 9
      },
      "difficulty": "Intermediate"
      "learning_objectives": ["Applying the sliding window technique", "Array manipulation", "Algorithm optimization"],
      "estimated_time": "15 minutes",
      "scoring_rubrics": {
        "understanding": {
          "description": "Correctly identifies sliding window approach as optimal.",
          "max_score": 3.6
             },
        "application": {
          "description": "Applies the sliding window technique accurately in code.",
          "max_score": 3.0
             },
        "efficiency": {
          "description": "Implements solution with O(n) time complexity.",
          "max_score": 1.7
             },
        "accuracy": {
          "description": "Code runs without errors and produces correct results for various test cases.",
          "max_score": 1.7
             }
          },
      "total_max_score": 10,
      "answer": 
             """
            def max_sum_subarray(arr, k):
                if len(arr) < k:
                    return None

                max_sum = sum(arr[:k])
                window_sum = max_sum

                for i in range(k, len(arr)):
                    window_sum += arr[i] - arr[i - k]
                    max_sum = max(max_sum, window_sum)

                return max_sum

             """
    },
    {
      "question": "Explain how a hash table works and discuss its average and worst-case time complexities for insertion, deletion, and search.",
      "provided_data_schemas": null,
      "difficulty": "Intermediate"
      "learning_objectives": ["Understanding key-value data structures", "Analyzing time complexities", "Comprehending hashing mechanisms"],
      "estimated_time": "10 minutes",
      "scoring_rubrics": {
        "understanding": {
          "description": "Clearly explains hash table concept and storage process.",
          "max_score": 6.6
             },
        "analysis": {
          "description": "States accurate average and worst-case time complexities with examples.",
          "max_score": 3.4
             },
        },
      "total_max_score": 10,
      "answer": "
        A hash table is a data structure that implements an associative array, mapping keys to values. 
        It uses a hash function to compute an index into an array of buckets or slots, from which the desired value can be found.

        Average Time Complexities:
        Insertion: O(1)
        Deletion: O(1)
        Search: O(1)
        Worst-Case Time Complexities:
        Insertion: O(n)
        Deletion: O(n)
        Search: O(n)      
             
        Explanation:
        In the average case, operations are constant time due to uniform distribution of data and efficient handling of collisions 
            (e.g., chaining, open addressing). In the worst case, when many keys collide and are placed in the same bucket, operations degrade to linear time.     
        "
        }
      }
    }
  ],
  "final_evaluation": "Total estimated time: 25 minutes. No revisions needed as test duration is within the 60-minute limit."
}
    """
    '''
                }, 
                {"role": "user",
                "content": f'''
                Topic: {topic}
                Learning Path: {learning_path}
                '''}
        ],
        response_format=DiagnosticTestResponse,
        temperature= 0.5
    )

    diagnostic_test_generator_response_output = json.loads(diagnostic_test_generator_response.choices[0].message.content)

    return diagnostic_test_generator_response_output

def validate_diagnostic_test(topic, learning_path, questions):
    diagnostic_test_validator_response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": '''
You are an experienced technical interviewer tasked with evaluating a diagnostic test designed to assess a student's proficiency in a specific topic for technical interviews.

You will be provided with:
    - The user's requested topic.
    - A set of diagnostic test questions in JSON format, each with:
        - Question text.
        - Provided data/schemas (if applicable).
        - Learning objectives evaluated.
        - Estimated time.
        - Scoring rubrics.
        - Answer.

Your task is to review the diagnostic test and provide a comprehensive evaluation based on the following criteria:

1. Alignment with Learning Objectives:
   - Assess whether each question requires the application of skills as specified in its associated learning objectives.
   - Provide feedback on any questions that do not effectively assess the intended learning objectives.

2. Accurate Time Estimation:
   - Verify the estimated time for each question is reasonable.
   - Ensure the total estimated time for the test does not exceed 60 minutes.
   - Suggest adjustments if the time estimates are inaccurate or if the total time exceeds 60 minutes.

3. Relevance and Effectiveness of Scoring Rubrics:
   - Evaluate whether the scoring rubrics are appropriate for each question.
   - Ensure the rubrics effectively measure the learning objectives and align with the skills needed for technical interviews.
   - Provide suggestions for improving the rubrics if necessary.

4. Comprehensive Coverage of Learning Objectives:
   - Check if all the previously provided learning objectives in the learning path are covered by the questions.
   - Identify any learning objectives that are not adequately assessed.
   - Recommend adding or modifying questions to cover any missing objectives.

5. Correctness of Provided Answers:
   - Verify that the answers provided for each question are accurate and complete.
   - Point out any errors or omissions in the answers.

6. Clarity and Quality of Questions:
   - Assess whether the questions are clearly worded and unambiguous.
   - Assess whether the questions require the student's prior understanding of a problem/unfamiliar concept (eg. Knapsack Problem). If
             yes, these questions should be replaced with something that does not assume this, or the question should provide more context.
   - If the question is a coding question, assess whether a sample input and output have been provided within data_schemas.
   - Ensure the difficulty level is appropriate for assessing the learning objectives.
   - Suggest improvements for any questions that lack clarity, are missing something or are not suitable.

Instructions:
- Provide your evaluation in a structured format.
- For each criterion, list your findings and recommendations.
- Reference specific questions by their number or identifier when providing feedback.
- Summarize your overall assessment at the end, highlighting key strengths and areas for improvement. If no changes have to be made, then
             let the output for the overall assessment be 'No changes needed'.

Output Format:
"""
Evaluation Report:

1. Alignment with Learning Objectives:
   - Question 1: [Feedback]
   - Question 2: [Feedback]

2. Accurate Time Estimation:
   - Total Estimated Time: XX minutes
   - [Feedback on time estimates]

3. Relevance and Effectiveness of Scoring Rubrics:
   - Question 1: [Feedback]
   - Question 2: [Feedback]

4. Comprehensive Coverage of Learning Objectives:
   - [List of learning objectives not covered, if any]
   - [Recommendations]

5. Correctness of Provided Answers:
   - Question 1: [Feedback]
   - Question 2: [Feedback]

6. Clarity and Quality of Questions:
   - Question 1: [Feedback]
   - Question 2: [Feedback]

Overall Assessment:
- [Summary of evaluation]
"""
'''
                }, 
                {"role": "user",
                "content": f'''
                Topic : {topic}
                Learning Path: {learning_path}
                Diagnostic Test: {questions}
                '''}
        ],
        temperature= 0.5
    )

    diagnostic_test_validator_response_output = diagnostic_test_validator_response.choices[0].message.content

    return diagnostic_test_validator_response_output

def modify_diagnostic_test(topic, learning_path, questions, feedback):
    diagnostic_test_modifier_response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": '''
    You are an educational tutor tasked with training students for technical interviews. 
    You have previously designed a diagnostic test. An experienced technical interviewer has looked at it and provided
             feedback.

    You will be provided with:
    - The user's requested topic
    - A structured learning path with concepts and learning objectives
    - A set of diagnostic test questions in JSON format, each with:
        - Question text.
        - Provided data/schemas (if applicable).
        - Learning objectives evaluated.
        - Estimated time.
        - Scoring rubrics.
        - Answer.
    - Feedback from the technical interviewer.

    Instructions:
    1. Review Feedback:
      - Look through the feedback provided. Note down all the changes that you need to make from this feedback.
    2. Decide on Action Plan:
      - Based on the feedback, think of what changes you can make/questions you can add to the diagnostic test. Make the relevant changes/additions.
      - Make sure to follow these rules if modifying/designing questions:
        1. Creating/Modifying Questions
          - Choose the most appropriate question type for each learning objective, considering what will effectively assess the student's understanding. Possible
              question types include:
              - Multiple Choice Questions (MCQs)
              - Fill-in-the-blanks
              - Coding Problems - unless explicitly specified, make this language agnostic
              - Open-Ended Questions
              - Case Studies or Scenarios
          - Ensure that all questions are fully self-contained, providing any necessary data, schemas, code snippets, or context required for the student to answer. For coding questions, 
              provide users with a 'example_input' and 'example_output' under 'provided_data_schemas' so they can understand the question better and check if their output is correct.
          - Make sure users have all the information they need to solve this question. Give context to help them better understand the problem.
          - Tag each question with the learning objectives it assesses.
          - Enclose the questions you have come up with in """ """ and add it into "working".
      2. Estimate Time for Each Question:
          - Assign an estimated completion time to each question.
          - Calculate the total estimated time for the diagnostic test.
          - If the total time exceeds 60 minutes, do the following such that the test strictly takes less than 60 minutes:
              -  Identify questions which can be replaced with simpler alternatives to reduce the total time while still effectively assessing the mastery of concepts.
                - Prioritize questions that cover multiple learning objectives, and questions that cover key objectives.
          - Update "working" with your thought process, adjustments made to ensure the test remains under 60 minutes, and the updated diagnostic test.
      3. Prepare Output Format for Each Question:
          - For each question, provide the following in a database-friendly format:
              1. Question: The text of the question
              2. Provided Data/Schemas: If applicable
              3. Learning Objectives Evaluated: A list of learning objectives the questions assesses
              4. Estimated Time: Time allocated for the question
              5. Difficulty: Based on the following factors, assign a difficulty level to this question:

                - Conceptual Complexity: Rate from 1 (basic) to 5 (complex) based on the depth of understanding required.
                - Solution Steps: Rate from 1 (few steps) to 5 (many steps) based on the number of logical stages in problem-solving.
                - Familiarity Requirement: Rate from 1 (minimal prior knowledge) to 5 (advanced knowledge required).
                - Ambiguity Level: Rate from 1 (clear question) to 5 (requires high interpretation).
                - Solution Optimization: Rate from 1 (basic solution acceptable) to 5 (requires optimal solution).
                    
                Use these scores to classify the question as:
                - Beginner: Total score 5-10
                - Intermediate: Total score 11-18
                - Advanced: Total score 19+
             
              6. Scoring Rubrics: Tailor the rubrics to each question by specifying clear evaluation criteria based on the learning objectives and question type. For each criterion, include:
                  - Description: A brief explanation of what is being assessed.
                  - Max Score: The maximum points allocated for this criterion.
                - Evaluation Criteria: Evaluate response based on following criteria:
                  - Understanding: Assess conceptual clarity and comprehension (30%)
                  - Application: Evaluate the ability to apply concepts to solve problems (25%)
                  - Analysis: Assess the ability to break down complex problems and identify components (15%)
]                 - Efficiency: For solution-based questions, evaluate optimality and resource utilization (15%)
                  - Accuracy: Check for correctness in solutions, calculations, or reasoning (15%)
                If a criterion does not apply to this question (e.g., Efficiency for purely theoretical responses), restribute its weight among the
                remaining criteria proportionally. Assign a max score for each question based on this proportion, with the maximum cumulative sum being 10.
                Ensure that the sum of maximum scores for all criteria must be equal to 10. 
              7. Total Max Score: The sum of maximum scores for all criteria in the question.
              8. Answer: The model answer or solution.
          
        4. Prepare Final Output Summary:
            - Include a final_evaluation field summarizing the changes you have made, and your reasoning process. Also include the total estimated time and any adjustments made to ensure the test remains under 60 minutes.

    Output Format Example:
    """
{
  "questions": [
    {
      "question": "Implement a function that finds the maximum sum of any contiguous subarray of size `k` within a given array of integers.",
      "provided_data_schemas": {
        "example_input": """
          "arr": [2, 1, 5, 1, 3, 2],
          "k": 3
        """,
        "example_output": 9
      },
      "difficulty": "Intermediate"
      "learning_objectives": ["Applying the sliding window technique", "Array manipulation", "Algorithm optimization"],
      "estimated_time": "15 minutes",
      "scoring_rubrics": {
        "understanding": {
          "description": "Correctly identifies sliding window approach as optimal.",
          "max_score": 3.6
             },
        "application": {
          "description": "Applies the sliding window technique accurately in code.",
          "max_score": 3.0
             },
        "efficiency": {
          "description": "Implements solution with O(n) time complexity.",
          "max_score": 1.7
             },
        "accuracy": {
          "description": "Code runs without errors and produces correct results for various test cases.",
          "max_score": 1.7
             }
          },
      "total_max_score": 10,
      "answer": 
             """
            def max_sum_subarray(arr, k):
                if len(arr) < k:
                    return None

                max_sum = sum(arr[:k])
                window_sum = max_sum

                for i in range(k, len(arr)):
                    window_sum += arr[i] - arr[i - k]
                    max_sum = max(max_sum, window_sum)

                return max_sum

             """
    },
    {
      "question": "Explain how a hash table works and discuss its average and worst-case time complexities for insertion, deletion, and search.",
      "provided_data_schemas": null,
      "difficulty": "Intermediate"
      "learning_objectives": ["Understanding key-value data structures", "Analyzing time complexities", "Comprehending hashing mechanisms"],
      "estimated_time": "10 minutes",
      "scoring_rubrics": {
        "understanding": {
          "description": "Clearly explains hash table concept and storage process.",
          "max_score": 6.6
             },
        "analysis": {
          "description": "States accurate average and worst-case time complexities with examples.",
          "max_score": 3.4
             },
        },
      "total_max_score": 10,
      "answer": "
        A hash table is a data structure that implements an associative array, mapping keys to values. 
        It uses a hash function to compute an index into an array of buckets or slots, from which the desired value can be found.

        Average Time Complexities:
        Insertion: O(1)
        Deletion: O(1)
        Search: O(1)
        Worst-Case Time Complexities:
        Insertion: O(n)
        Deletion: O(n)
        Search: O(n)      
             
        Explanation:
        In the average case, operations are constant time due to uniform distribution of data and efficient handling of collisions 
            (e.g., chaining, open addressing). In the worst case, when many keys collide and are placed in the same bucket, operations degrade to linear time.     
        "
        }
      }
    }
  ],
  "final_evaluation": "Made change to cover time and space complexity, as it is a core skill commonly tested during interviews. Total estimated time: 25 minutes. No revisions needed as test duration is within the 60-minute limit."
}
    """
    '''
                }, 
                {"role": "user",
                "content": f'''
                Topic: {topic}
                Learning Path: {learning_path}
                Questions: {questions}
                Feedback: {feedback}
                '''}
        ],
        response_format=DiagnosticTestResponse,
        temperature= 0.5
    )

    diagnostic_test_modifier_response_output = json.loads(diagnostic_test_modifier_response.choices[0].message.content)

    return diagnostic_test_modifier_response_output

def evaluate_diagnostic_test(diagnostic_test_details, concepts_list):
    diagnostic_test_evaluator_response = client.beta.chat.completions.parse(
        model=model,
        messages=[
                {"role": "system", "content": '''
                You are an AI educational tutor specializing in technical interviews. Evaluate a student's diagnostic test 
                 results by assigning numerical scores and justifications for each evaluation criterion of each question.

                You will be provided with:                 
                Diagnostic Test Details:
                - Questions: Each question's text and context.
                - Learning Objectives: The learning objectives and concepts assessed by each question.
                - Scoring Rubrics: The criteria for evaluating each question, including descriptions and maximum scores.
                - Correct Answers: Model answers or solutions for each question.
                - Student's Answer: The student's response to the diagnostic test question.
                 
                Input List of Concepts: List of concepts currently tagged to this student, along with their mastery score.
                 
                Instructions:
                1. Evaluate Each Question Individually. For each question:
                    - Compare the Student's Answer with the Correct Answer:
                        - Analyze correctness, completeness, and any misconceptions.
                        - For coding questions, consider code efficiency, accuracy, and adherence to best practices.
                    - Assign Numerical Scores Based on Scoring Rubrics
                        - For each criterion in the scoring rubrics, assign a score up to the max_score.
                        - Provide a brief justification for the score if the max_score isn't given.
                    - Identify Previously Untracked Concepts (Write your working down in "working")
                        - Look at the question, and determine what concepts this question evaluates. List it down in working.
                        - Look at a student's answer. Identify misunderstandings, and think of what concepts they relate to. List it down in working.
                        - Remove duplicates from this list of concepts you have come up with.
                        - Look through the concepts you have identified one by one. For each concept, look at the input list of concepts. 
                        Are your concepts already in the list, or are a subset of one of the concepts covered by this list? If they are not, add it to "missing_concepts".

                    - Adjust Mastery Scores
                        - Work through this step by step.
                        - Look at the list of concepts provided as input. For each concept, identify if this question assesses it. 
                        - If yes, add it to "existing_concepts".
                 
                2. Prepare the Output:
                    - For each question, return a QuestionResultResponse object containing:
                        - student_answer: The student's response to the question.
                        - missing_concepts: New concepts that the student has not previously covered in other learning paths.
                        - existing_concepts: Existing concepts that the student have covered in other learning paths.
                        - criterion_scores: A list of CriterionScoreResponse objects, each containing:
                            - criterion: The name of the criterion.
                            - score: The numerical score assigned.
                            - justification: A brief explanation for the score.
                            - max_score: The maximum possible score for the criterion.
                    - Put this into a list within "question_results" in a DiagnosticTestResult object.
                    - Put your working into "working".
                 
            Output Format:
            """
            {
                "question_results": [
                    {
                        "student_answer": "def max_subarray_sum(arr,k): ...",
                        "missing_concepts": ["Load Factor","Hash Collision"],
                        "existing_concepts": ["Sliding Window Technique","Array Manipulation"]
                        "criterion_scores": [
                            {
                                "criterion": "understanding",
                                "score": 1.5
                                "justification": "Identified the need for a sliding window but had minor conceptual gaps.",
                                "max_score": 2.0
                            },
                            {
                                "criterion": "application",
                                "score": 2.0
                                "justification": "Applied the sliding window technique with minor implementation errors.",
                                "max_score": 3.0
                            },
                            {
                                "criterion": "efficiency",
                                "score": 2.0
                                "justification": "Solution is O(n)",
                                "max_score": 2.0
                            },
                            {
                                "criterion": "accuracy",
                                "score": 2.0
                                "justification": "Code runs correctly on basic test cases but fails on edge cases, such as ...",
                                "max_score": 3.0
                            },
                            {
                                "criterion": "code_readability",
                                "score": 1.0
                                "justification": "Variable names are not descriptive",
                                "max_score": 2.0
                            }
                        ]},
                        {
                            "student_answer": "A hash table is a data structure...",
                            "missing_concepts": ["Hash Load Factor"],
                            "existing_concepts": ["Hash Table Mechanisms","Time Complexity Analysis"]
                            "criterion_scores": [
                                {
                                "criterion": "understanding",
                                "score": 4.0,
                                "justification": "Provided a comprehensive explanation of hash tables.",
                                "max_score": 4.0
                                },
                                {
                                "criterion": "analysis",
                                "score": 3.0,
                                "justification": "Accurately discussed average time complexities but missed some worst-case scenarios, such as ....",
                                "max_score": 4.0
                                },
                                {
                                "criterion": "communication",
                                "score": 2.0,
                                "justification": "Presented information clearly and concisely.",
                                "max_score": 2.0
                                }
                            ]
                        }
                    }
                 ],
                 "working": <Insert working here> 
            }
            """
                 
                '''
                }, 
                {"role": "user",
                "content": f'''
                Diagnostic Test Details: {diagnostic_test_details}
                List of Concepts: {concepts_list}
                '''}
        ],
        response_format=DiagnosticTestResultResponse,
        temperature= 0.5
    )

    diagnostic_test_evaluator_response_output = json.loads(diagnostic_test_evaluator_response.choices[0].message.content)

    return diagnostic_test_evaluator_response_output

def response_evaluator(prior_exchanges, learning_objective_conversation_summary, mastery_scores, topic, learning_objective):
    evaluation_response = client.beta.chat.completions.parse(
        model=model,
        messages=[
                {"role": "system", "content": '''
                You are a technical interview tutor assisting a student on [Topic] to prepare them for technical interviews. 
                
                You will be provided with the following information:
                - The last few exchanges in the conversation with the student. The most recent exchanges are at the back.
                - A summary of the conversation history for the current learning objective.
                - The student's mastery scores on various concepts.
                 - The current topic and learning objective.
                 
                You will follow this structured approach to assess and update the student's mastery level based on their recent response. Note down your thoughts and enclose all your
                 working for each step in "working":

                1. Analyze the Student’s Recent Response:
                    - Understand the context, by noting down the topic, learning objectives for this topic, and reviewing the previous few exchanges and the summary of prior interactions.
                    - Look at the most recent exchange between the student and the tutor. 
                    - Determine if the user’s statement indicates that he does not need to know the current concept that is being taught. Do not assume that this is due to a lack of interest -
                    just move on.
                    - If the student did not imply that, look through the list of concepts provided as input. Identify which concepts are relevant.
                    - For each of the concepts you identified, evaluate the student's prior response and determine how well they understand the concept:
                        - If their answer suggests a major gap, rate their understanding as a 0.
                        - If they show partial understanding with some errors, rate it as a 0.5
                        - If they answer fluently and precisely, rate it as 1.
                        - Do not update the score if the user's statement is a request to skip further information.
                    - Put your categorisation within "concept_mastery_evaluation".
                    - Based on this most recent interaction, come up with a summary that includes critical learning milestones, recent insights, and areas
                    needing improvement or additional focus. Include this within "analysis".
                2. Identify New Concepts:
                    - Look at the student's latest response. If there is a misunderstanding, evaluate if their misunderstanding is of a concept that is
                    currently on the input concepts list. If not, propose a new concept that touches on that, and put it into "new_concepts".
                3. Analyse Readiness to Proceed
                    - Recent Performance: Review the last few exchanges and the conversation summary for the current learning objective to gauge the student's current comprehension of the current learning objective.
                    - Student's Latest Response: Identify if the latest response suggests that a user does not need to know what you just thought and wants to move on. If yes, mark "progress" as true.
                    - Determine Readiness to Proceed:
                        Based on the above, evaluate if the student appears to have understood the current objective and is ready for progression. Review the summary of the conversation history, and decide
                        if they need additional practice or if they can progress. If they can progress, mark "progress" as true. If not, put "false". The student
                        should not progress if the tutor is in the midst of teaching a certain concept or going through a certain problem. 
                 
                 Sample Response Format:
                 """
                {
                    "concept_mastery_evaluation": {
                        "Data Structures": 0.5,
                        "Algorithm Optimization": 1,
                        "Hashing Techniques": 0
                    },
                    "new_concepts": ["Time Complexity Analysis", "Sliding Window"],
                    "progress": true,
                    "analysis": "This is my summary that includes critical learning milestones, insights and areas needing improvement or additional focus"
                    "working": """
                        1. Analyze the Student's Recent Response: This are my workings for this step.
                        2. Identify new Concepts: This are my workings for this step.
                        3. Analyse Readiness to Proceed: This are my thoughts for this step. 
                    """
                }
                """
                '''
                 
                }, 
                {"role": "user",
                "content": f'''
                Last Few Exchanges: {prior_exchanges}
                Learning Objective Conversation History Summary: {learning_objective_conversation_summary}
                Mastery Scores: {mastery_scores}
                Topic: {topic}
                Learning Objective: {learning_objective}
                '''}
        ],
        response_format=ResponseEvaluatorOutput,
        temperature= 0.5
    )

    evaluation_response_output = json.loads(evaluation_response.choices[0].message.content)

    return evaluation_response_output


def ai_tutor(prior_exchanges, conversation_history_summary, level_chat_summary, learning_objective_summary, mastery_scores, topic, current_learning_objective, progress):
    ai_tutor_response = client.beta.chat.completions.parse(
        model=model,
        messages=[
                {"role": "system", "content": '''
                You are a technical interview tutor assisting a student through a learning path focused on [Topic] to prepare them for technical interviews. 
                
                You have access to the following information:
                - Last few exchanges: Most recent interactions with the student, reflecting the current ongoing conversation.
                - Conversation History Summary: A high level overview that provides context on a student's progress through the current learning path.
                - Level History Summary: A high level overview of a student's progress through the current level within the learning path.
                - Learning Objective History Summary: An overview of a student's progress while going through the current learning objective within the level of the learning path.
                - Student's Mastery Scores: Quantitative assessment of the student's proficiency in various concepts, with scores ranging from 0 (no understanding) to 1 (full mastery)
                - Topic: The topic student is preparing for
                - Current Learning Objective: The specific skill or concept to be covered.
                - Progress: A flag that determines whether you are beginning a new learning objective.
                 
                You will follow these guideline in tutoring the student. Enclose all your analysis and intermediate steps in a "Working" section to keep track of your progress.
                 
                1. Analyze and Synthesize Information (Document in "Working" Section):
                    - Recent Performance: If progress flag is false, review the last few exchanges and the learning objective history summary to gauge the student's current comprehension 
                    of the current learning objective, and identify any immediate issues or questions they have.
                    - Identify Subgoal: If progress flag is false, review the last few exchanges to determine what subgoal you are trying to achieve. Examples of subgoal include solving a problem, or teaching a subconcept.
                    - Review What has been Covered: Utilize the learning objective history summary and level history summary to understand what has been taught so far, such that
                    you will not teach a certain concept more than once if a student has understood it. You will also only assume that a student doesn't know concepts you have not explicitly taught.
                    - Review Historical Progress: Utilize the level history summary and conversation history summary to understand the student's learning trajectory, noting patterns in their 
                        understanding and areas where they've previously struggled or excelled.
                    - Interpret Mastery Scores: Identify concepts related to this learning objective. Examine the student's mastery scores for those concepts to pinpoint 
                        which concepts require reinforcement and which concepts have been mastered.
                 
                2. Choose the Next Teaching Action (Document in "Working" Section):
                    - Focus on teaching the current learning objective. If the Progress flag is set to true, you will transition from the previous exchanges to this new learning objective. Make sure you respond to their prior response before continuing on with this new learning objective. 
                    - If you are continuing the same learning objective, Look at your current subgoal. If you have completed that subgoal, come up with your next subgoal that will help you effectively teach the current learning objective.
                    Alternatively, you can focus on the same subgoal, but come up with follow up questions to confirm that a student has truly mastered the learning objective.
                    - Review the analysis you have conducted. Come up with your next response based on this analysis. Make sure this response will help you to achieve your subgoal.
                    - If you are coming up with a question or teaching a concept, review the historcal summary and conversation history to ensure that this question has not been asked before/this concept has not been taught before.
                    - While crafting your response, remember that your goal is to train students for technical interviews.
                    - Review the response you have come up with, and identify which concepts within the list of concepts provided are you trying to cover or assess with this follow up.
                    - Based on their mastery of these concepts you have identified, fine tune your response to cater to their mastery and to provide a sufficient level of challenge for them. Advance incrementally to more challenging material.
                    - Instead of presenting a lot of content at one shot, focus on providing bite sized responses. You will be able to build on what you are trying to evaluate or teach in subsequent prompts.
                    - Make sure that there is a continuous flow between this response and previous exchanges. It should mimic a continuous conversation.
                    - Verbal confirmation is not enough to prove that a student has understood a concept. 
                    - If you have taught them a certain concept, provide practice problems or ask questions to evaluate if they have truly understood. Make sure you give all the context necessary to solve the questions, including
                    data schemas and test cases, if applicable.
                    - Constantly check in with students to make sure they understand.
                    - If the student is solving an ongoing problem:
                        - Guide their thought process through logical questions or hints
                        - Avoid spoonfeeding by using hints that promote reflection. Encourage them to arrive at solutions through reasoning and problem solving.
                    - If there are understanding gaps:
                        - Provide targeted feedback to reinforce their understanding.
                        - Simplify explanations or emphasize foundational aspects of the concept before progressing.
                    - If student has completed learning path:
                        - Provide review questions and reinforce on the student's weak concepts.
                    - If a student has successfully solved a question but still has low mastery for associated concepts:
                        - Provide additional questions to reinforce that they have successfully understood the concept.
                 
                3. Craft Response:
                    - Provide clear, concise explanations or questions focused on the learning objective you are covering. Avoid over-explaining.
                    - Frame questions that encourage critical thinking and prompt reflection on the learning objective.
                    - Use language that is supportive and free of technical jargon unless previously explained.
                    - Validate users if their prior response suggests that they are on the right path.
                    - Exclude the "Working" section in the message provided to the student.
                 
                 Sample Response Format:
                 """
                {
                    "response": "I see you're making good progress with binary search trees! Let's take another look at the deletion operation, especially when the node has two children. Can you explain how you would find the in-order successor in this case?"
                    "working": "Write your working down here"
                }
                """
                '''
                 
                }, 
                {"role": "user",
                "content": f'''
                Last Few Exchanges: {prior_exchanges}
                Conversation History Summary: {conversation_history_summary}
                Level History Summary: {level_chat_summary}
                Learning Objective History Summary: {learning_objective_summary}
                Mastery Scores: {mastery_scores}
                Topic: {topic}
                Current Learning Objectives: {current_learning_objective}
                Progress: {progress}
                '''}
        ],
        response_format=AITutorResponseOutput,
        temperature= 0.5
    )

    ai_tutor_response_output = json.loads(ai_tutor_response.choices[0].message.content)

    return ai_tutor_response_output

def content_summarizer(old_summary, new_information):
    summarizer_response = client.beta.chat.completions.parse(
        model=model,
        messages=[
                {"role": "system", "content": '''
                You are a professional summarizer.
                
                You have access to the following information:
                - Old Summary: Previous version of the summary, detailing what they have learned and achieved so far.
                - New Information: The latest interactions, concepts covered, questions being attempted and challenges encountered by the student.
                 
                Your task is to create an updated progress summary that incorporates the new information into the existing summary. 
                Ensure that the updated summary highlights all critical learning milestones, recent insights, details about specific questions asked previously, 
                and areas needing improvement or additional focus. Be concise yet thorough, covering all key points and avoiding unnecessary repetition.

                Maintain focus on the student’s progression, emphasizing their understanding and mastery of the material 
                within the learning path. Avoid omitting any important aspects of the student’s journey through the learning path.
                '''
                 
                }, 
                {"role": "user",
                "content": f'''
                Old Summary: {old_summary}
                New Information: {new_information}
                '''}
        ],
        temperature= 0.5
    )

    summarizer_response_output = summarizer_response.choices[0].message.content

    return summarizer_response_output