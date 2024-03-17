import os
# Update the import statement for Ollama from langchain-community
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process

# Load local model through Ollama
mistral = Ollama(model="mistral")

# Cybersecurity Analyst Agent
cve_analyst = Agent(
    role="Cybersecurity Analyst",
    goal="Identify and analyze the latest CVEs related to IoT and CCTV systems",
    backstory="""As a cybersecurity analyst with extensive experience in system vulnerabilities and risk assessment, you are tasked with analyzing 
    system configurations and CVE details to identify potential compromises. Your expertise lies in dissecting CVE reports, understanding their 
    implications on IoT and CCTV systems, and devising strategic advice for mitigating risks.""",
    verbose=True,
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
    and provide advice for IoT system security improvements. Include good security practices and recommendations for mitigating identified vulnerabilities.""",
    expected_output="A detailed report with vulnerabilities, security advice, and mitigation strategies.",
    agent=report_generator,
)

# Setup the crew with the new tasks and agents
cve_crew = Crew(
    agents=[cve_analyst, report_generator],
    tasks=[task_search_analyze, task_report_generation],
    verbose=2,
    process=Process.sequential,
)

# Kick off the process
result = cve_crew.kickoff()

print("######################")
print(result)
