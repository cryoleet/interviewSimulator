import google.generativeai as genai
import json


topicListPrompt = """
I have a list of keywords. For each keyword, generate an interview question related to that keyword. The questions should be relevant, professional, and appropriate for a job interview.

Keywords: {}
"""



companySpecificPrompt = """
Generate a list of {} questions that is most likely to be asked in an interview at {}
for the role {}

Format the output as a list of questions, separated by a single newline character and nothing else. Do not include any extra text, just the questions
"""


JdPrompt = """
Here's text that has been extracted from a job description file, extract useful information from this text and generate a list of {} questions for the job described.

"{}"

Format the output as a list of questions, separated by a single newline character and nothing else. Do not include any extra text, just the questions
"""


questions_schema = {
    "type": "array",
    "items": {"type": "string"}
}

# feedbackPrompt = """
# Below is a python dictionary in string format, where each key represent a question and value represents an answer given by a user of a platform.

# {}

# the output should be in the following format: it should be a json object, where the key is the question number and the value is another json object consisting of a feedback attribute and confidence attribute, the feedback attribute should be a succint paragraph that gives feedback on the answer given by the user for the given question, in case of objective questions give feedback on how accurate the answer is and where it could be better, in case of subjective questions give feedback on how well the user answered and what could it done better. The confidence attribute should be a number out of 5, depending on how confident you think the user's answer was.


# Keep in mind that the user's answer are generated from a speech-to-text model, if the answer is no way related to the question or if it is inteligible, the feeback attribute should say "Invalid answer" and the confidence score should be -1.

# The reponse text should be directly parsable using json.loads() in python.
# """

feedback_obj = {
  "type" : "object",
  "properties" : {
    "question" : {"type" : "string"},
    "answer" : {"type" : "string"},
    "accuracy" : {"type" : "string"},
    "grammar" : {"type" : "string"},
    "confidence" : {"type" : "integer"}
  },
  "required" : ["question", "answer", "accuracy", "grammar", "confidence"]
}

feedback_schema = {
    "type" : "array",
    "items" : feedback_obj
}

feedbackPrompt = """
Below is a Python dictionary in string format, where each key represents a question, and the corresponding value is the answer given by a user on a platform.

{}

return json response
For each answer, provide feedback including the following fields:

question - the question itself
answer - the answer given by the user
Accuracy - If the question has an objective answer describe how accurate the answer was and where it could be improved, if the answer is subjective describe how well the user answered and where they could improve. This should be a succint paragraph.
Grammar - A succint paragraph highlighting the major grammatical errors in the user's answer.
confidence - a number in the range 1-5 based on how confident the answer was

Provide the feedback for each question-answer pair in chronological order.
"""




def askGemini(prompt, schema):
  genai.configure(api_key="AIzaSyAQU_hoYRlc74gZFO6ehzbe1lGgvbZdqn8")
  model = genai.GenerativeModel("gemini-1.5-flash")
  response = model.generate_content(
    prompt,
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=schema
    ),
  )
  return json.loads(response.text)


