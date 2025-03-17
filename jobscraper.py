import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv
import schedule
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import datetime

# Load environment variables
load_dotenv()

# Fetch API keys from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "")

if not GEMINI_API_KEY:
    print("❌ Error: GEMINI_API_KEY is missing. Check your .env file.")
    exit(1)

if not SLACK_BOT_TOKEN or not SLACK_CHANNEL:
    raise ValueError("❌ Missing Slack bot token or channel in .env file.")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# Slack client setup
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# Base URL (Modify if necessary)
BASE_URL = "https://talenthubsolutions.com/?jb-page%5B1%5D="

# Paginated URL
MAX_JOBS = 10  # Target job count

def fetch_job_listings():
    """Scrape at least 20 job listings from multiple pages."""
    try:
        print("🔎 Fetching job listings...")
        jobs = []
        page = 1  # Start from the first page
        while len(jobs) < MAX_JOBS:
            page_url = f"{BASE_URL}{page}"  # Construct paginated URL
            print(f"🌐 Fetching page {page}: {page_url}")
            response = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if response.status_code != 200:
                print(f"❌ Failed to fetch jobs from page {page}. Status code: {response.status_code}")
                break  # Stop if the request fails
            soup = BeautifulSoup(response.text, "html.parser")
            job_elements = soup.select(".jb-job-title-link")
            if not job_elements:
                print(f"⚠️ No jobs found on page {page}. Stopping search.")
                break  # Stop if no jobs are found
            for job in job_elements:
                if len(jobs) >= MAX_JOBS:
                    break  # Stop when 20 jobs are collected
                title = job.text.strip()
                link = urljoin(page_url, job.get("href"))  # Ensure absolute URL
                print(f"📌 ({len(jobs) + 1}/{MAX_JOBS}) Fetching details for: {title}")
                # Fetch job description
                job_response = requests.get(link, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                if job_response.status_code != 200:
                    print(f"⚠️ Failed to fetch job details for {title}. Status: {job_response.status_code}")
                    description = "No description available."
                else:
                    job_soup = BeautifulSoup(job_response.text, "html.parser")
                    desc_elem = job_soup.select_one(".entry-content")
                    if desc_elem:
                        paragraphs = [p.get_text(strip=True) for p in desc_elem.find_all("p")]
                        description = "\n\n".join(paragraphs).strip()
                    else:
                        description = "No description available."

                # Extract location and apply link (if possible)
                location = "Not specified"  # Default location
                apply_link = ""
                if "Location:" in description:
                    location_start = description.find("Location:") + len("Location:")
                    location_end = description.find("\n", location_start)
                    if location_end == -1:
                        location = description[location_start:].strip()
                    else:
                        location = description[location_start:location_end].strip()

                if "email your details to" in description:
                    apply_start = description.find("email your details to") + len("email your details to")
                    apply_end = description.find(".",apply_start)+1
                    if apply_end == 0:
                      apply_end = len(description)

                    email = description[apply_start:apply_end].strip()
                    apply_link = "mailto:" + email

                jobs.append({
                    "title": title,
                    "location": location,
                    "description": description,
                    "apply_link": apply_link,
                    "job_link": link
                })
            page += 1  # Move to the next page
        print(f"\n✅ Successfully fetched {len(jobs)} job listings.")
        return jobs
    except Exception as e:
        print(f"🚨 Error fetching jobs: {e}")
        return []

def analyze_jobs_with_gemini(jobs):
    """Sends job data to Gemini AI for analysis and prints key insights."""
    try:
        # Initialize the model (Use "gemini-1.5-flash" for free tier)
        model = genai.GenerativeModel("gemini-1.5-flash")  # Use "gemini-1.5-pro" for better responses

        # Convert job data to JSON string
        jobs_json = json.dumps(jobs)

        # Send a request to Gemini AI
        response = model.generate_content(f"Analyze the following job listings and format each job like this:\n\n(job no.)Job Title: [Job Title]\nJob Description: [Short Job Description]\nApply Link: [Apply Link]\n\n{jobs_json}")

        # Print the response
        print("✅ Gemini AI Response:\n", response.text)
        return response.text #return the response

    except Exception as e:
        print(f"🚨 Gemini AI error: {e}")
        return None

def send_to_slack(message):
    """Send message to Slack."""
    try:
        response = slack_client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        if response["ok"]:
            print(f"✅ Message sent to Slack")
    except SlackApiError as e:
        print(f"❌ Error sending to Slack: {e.response['error']}")

def run_job():
    """Runs all processes and sends data to Slack."""
    print(f"Running job at {datetime.datetime.now()}")
    job_data = fetch_job_listings()
    if job_data:
        gemini_response = analyze_jobs_with_gemini(job_data)
        if gemini_response:
            send_to_slack(gemini_response)

# Schedule the job to run at 5:00 AM every day
schedule.every().day.at("23:40").do(run_job)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
