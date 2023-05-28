import requests
import console
from bs4 import BeautifulSoup

# search for jobs on Indeed and apply to them
def search_and_apply_jobs(resume_url, job_title, keywords):
    # Create a session to persist the cookies across requests
    session = requests.Session()

    # Fetch the user's resume page
    response = session.get(resume_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the resume content
    resume_data = {}
    resume_data['name'] = soup.find('div', class_='rezemp-ResumeDisplay-name').text.strip()
    resume_data['email'] = soup.find('div', class_='rezemp-ResumeDisplay-email').text.strip()
    resume_data['phone'] = soup.find('div', class_='rezemp-ResumeDisplay-phone').text.strip()

    # Extract skills section from the resume
    skills_section = soup.find('section', class_='rezemp-uHPrNK')

    # Extract the skills from the skills section
    skills = []
    if skills_section:
        skills = [skill.text.strip().lower() for skill in skills_section.find_all('span', class_='rezemp-ResumeSkill-item')]

    # Get the search page
    search_url = f"https://www.indeed.com/jobs?q={job_title}"
    response = session.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all job listings on the search page
    job_listings = soup.find_all('div', class_='jobsearch-SerpJobCard')

    for job_listing in job_listings:
        # Extract the job title and description
        title = job_listing.find('h2', class_='title').text.strip().lower()
        description = job_listing.find('div', class_='summary').text.strip().lower()

        # Check if the job matches the keywords from the skills section
        if all(keyword.lower() in description or keyword.lower() in title for keyword in keywords):
            # Get the apply URL for the job
            apply_url = "https://www.indeed.com" + job_listing.find('a')['href']

            # Get the job details page
            response = session.get(apply_url)
            job_soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the job's application form data
            form = job_soup.find('form', id='applyButtonLinkContainerForm')
            form_data = {input_field['name']: input_field.get('value', '') for input_field in form.find_all('input')}

            # Submit the job application
            response = session.post(apply_url, data={**form_data, **resume_data})
            
            # Handle the response as needed (e.g., check for success or error messages)

# Example usage
job_title = 'software engineer'
keywords = ['python', 'java', 'web development']

resume_url = console.input_alert("Enter the URL to your Indeed resume", "Resume URL")
search_and_apply_jobs(resume_url, job_title, keywords)
