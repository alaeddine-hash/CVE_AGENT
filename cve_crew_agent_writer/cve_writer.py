import os
# Update the import statement for Ollama from langchain-community
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process

# Importing crewAI tools
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool
)

# Set up API keys
os.environ["SERPER_API_KEY"] = "a11cd3e9c0db13f722d48c414ec5276850f7c765" # serper.dev API key
# Load local model through Ollama
mistral = Ollama(model="mistral")

# Instantiate tools
docs_tool = DirectoryReadTool(directory='./blog-posts')
file_tool = FileReadTool()
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()

# Cybersecurity Analyst Agent
cve_analyst = Agent(
    role="Cybersecurity Analyst",
    goal="Identify and analyze the latest CVEs related to IoT and CCTV systems",
    backstory="""As a cybersecurity analyst with extensive experience in system vulnerabilities and risk assessment, you are tasked with analyzing 
    system configurations and CVE details to identify potential compromises. Your expertise lies in dissecting CVE reports, understanding their 
    implications on IoT and CCTV systems, and devising strategic advice for mitigating risks.""",
    verbose=True,
    tools=[search_tool, web_rag_tool],
    allow_delegation=True,
    llm=mistral
)

# Vulnerability Analysis and Report Generation Agent
report_generator = Agent(
    role="Report Generator",
    goal="Generate a comprehensive report based on the CVE analysis with advice for IoT system security improvement",
    backstory="""With a deep understanding of cybersecurity practices and the ability to translate technical findings into actionable advice, 
    you specialize in creating detailed reports. These reports not only highlight vulnerabilities but also provide step-by-step guidance on enhancing 
    security postures for IoT and CCTV systems.""",
    verbose=True,
    tools=[search_tool, web_rag_tool],
    allow_delegation=True,
    llm=mistral
)

writer = Agent(
    role='Content Writer',
    goal='Craft engaging blog posts about the AI industry',
    backstory='A skilled writer with a passion for technology.',
    tools=[docs_tool, file_tool],
    verbose=True,
    allow_delegation=True,
    llm=mistral
)



# Task to search and analyze CVEs with expected_output added
task_search_analyze = Task(
    description="""Scrape web for searching the latest IoT and CCTV CVEs. Analyze these CVEs to identify the type of vulnerability (e.g., SQL injection, 
    buffer overflow), the components of the system likely affected, and assess the impact level (high, medium, low) on the system.""",
    expected_output="A summary of identified vulnerabilities, including types, affected components, and impact levels.",
    agent=cve_analyst,
)

# Task to generate a comprehensive report with expected_output added
task_report_generation = Task(
    description="""Using the analysis from the previous task, generate a comprehensive report detailing the identified vulnerabilities, affected components,
    and provide advice for IoT system security improvements. Include good security practices and recommendations for mitigating identified vulnerabilities.
    like reports i json format""",
    expected_output="A detailed report with vulnerabilities, security advice, and mitigation strategies.",
    agent=report_generator,
)

write_task = Task(
    description='Using the reports from the previous task Write an engaging blog post about the security industry, based on the Report Generator’s summary.',
    expected_output='A 4-paragraph blog post formatted in markdown with engaging, informative, and accessible content, avoiding complex jargon, and provide then cves in valid json formats',
    agent=writer,
    output_file='blog-posts/new_post.md'  # The final blog post will be saved here
)

# Setup the crew with the new tasks and agents
cve_crew = Crew(
    agents=[cve_analyst, report_generator, writer],
    tasks=[task_search_analyze, task_report_generation, write_task],
    verbose=True,
    
)


# Kick off the process
result = cve_crew.kickoff()

print("######################APAIA-TECKNOLOGIY##################MANSOURI######")
print(result)
