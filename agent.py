import warnings
import os
warnings.filterwarnings("ignore")
from crewai import Agent, Task, Crew
from dotenv import load_dotenv  # Add this import
load_dotenv()  # Update this line

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_MODEL_NAME'] = 'gpt-3.5-turbo'

print(OPENAI_API_KEY)

planner = Agent(
    role="Content planner",
    goal="Plan engaging and factually accurate content on a {topic} ",
    backstory="you are working on planning a blog article about the {topic}"
    " you collect information that helps the "
    "audience learn something"
    "and make informed decisions. Your work is the basis for the Content writer to write an article on this topic  ",
    allow_delegation=False,
    verbose=True

)
writer = Agent(
    role="Content writer",
    goal="Write insightful and factually accurate opinion piece about the topic: {topic} ",
    backstory="you are working on writing a new opinion piece about the topic: {topic} "
    "you base your work on the output of the Content Planner who provides an outline "
    " and relevant context about the topic you follow main objectives and direction of the outline"
    "as provided by the content planner. You also provode objective and impartial insights and back them up with "
    "information provided by the content planner."
    "You acknowledge in your opinion piece when your statemets are opinions as opposed to objective statements",
    allow_delegation=False,
    verbose=True

)

editor = Agent(
    role="Editor",
    goal="Edit a given post to align with the writing style of the organization. ",
    backstory="you are an editor who receives a blog post from the content writer.  "
    "your goal is to review the blog post to ensure that is follows the journalistic best practices,"
    "provides balanced view points "
    "when providing opinions or assertions, and also avoids major controversial topics "
    "or opinions when posiible.",
    allow_delegation=False,
    verbose=True


)
plan = Task(
    description=
      "1. Prioritize the latest trends, key players, "
          "and noteworthy news on {topic}.\n"
      "2. Identify the target audience, concidering their interests and pain points.\n "
      "3. Develop a detailed content outline including and introduction, key points, and a call to action. \n"
      "4. Include SEO keywords and relevant data or sources."
    ,
    expected_output="A comprehensive content plan document with an outline, audience analysis, SEO keywords, and resources",
    agent= planner
)

write = Task(
    description=
        ("1. Use the content plan to craft a complelling blog post on {topic}.\n"
        "2. Sections sub titles are properly named in an egaging manner.\n"
        "3. Ensure the post is structured with an engaging introduction \n"
        "4. Proofread for grammatical errors and alignment with brand voice.\n"),

    expected_output="A well-written blog post in markdown format, ready for publication,"
                    "each section should have 2 or 3 paragraphs",
    agent=writer
)

edit = Task(
    description=("Proofread the given blog post for grammatical errors and alignment with the brand voice"),
    expected_output="A well-written blogpost in markdown format"
                    "ready for publication, each section should have 2 or 3 paragraphs",
    agent=editor
)

crew = Crew(agents=[planner, writer, editor], tasks=[plan, write, edit], verbose=True)

##result = crew.kickoff(inputs={"topic":"Artifitial Intelligence"})

topic = "Job search for Entry level Java professionals"
result = crew.kickoff(inputs={"topic": topic})
