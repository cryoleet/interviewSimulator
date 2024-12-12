import google.generativeai as genai


topicListPrompt = """
I have a list of keywords. For each keyword, generate an interview question related to that keyword. The questions should be relevant, professional, and appropriate for a job interview.

Keywords: {}

Format the output as a list of questions, separated by a single newline character and nothing else. Do not include any extra text, just the questions.
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


def askGemini(prompt) -> list[str]:
  genai.configure(api_key="AIzaSyAQU_hoYRlc74gZFO6ehzbe1lGgvbZdqn8")
  model = genai.GenerativeModel("gemini-1.5-flash")
  response = model.generate_content(prompt)
  list_of_questions = [x for x in response.text.split("\n") if x != '']
  return list_of_questions