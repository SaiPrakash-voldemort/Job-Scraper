# Job Scraper & AI-Based Analysis

## 📌 Overview
This project automates job listing extraction, analysis, and sharing using web scraping, AI processing, and Slack integration. It scrapes job listings from **Talent Hub Solutions**, analyzes them using **Gemini AI**, and sends the refined results to a **Slack channel** every day at **5:00 AM**.

## 🛠️ Tech Stack
- **Python** (Core language)
- **BeautifulSoup** (Web Scraping)
- **Requests** (HTTP Requests)
- **Google Gemini AI** (Job Description Analysis)
- **Slack SDK** (Slack Integration)
- **Schedule** (Task Scheduling)
- **Dotenv** (Environment Variable Management)

## 📌 Features
- **Scrapes Job Listings**: Extracts jobs from multiple pages.
- **Analyzes with AI**: Summarizes job descriptions using **Gemini AI**.
- **Slack Integration**: Sends analyzed results to a configured Slack channel.
- **Automatic Execution**: Runs daily at **5:00 AM**.

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/SaiPrakash-voldemort/job-scraper-ai.git
cd job-scraper-ai
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables
Create a `.env` file in the project root and add:
```ini
GEMINI_API_KEY=your_gemini_api_key
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_CHANNEL=your_slack_channel_id
```

### 4️⃣ Run the Script Manually
```sh
python main.py
```

## 📜 How It Works
1. **Scrapes job postings** from Talent Hub Solutions.
2. **Extracts details**: Title, location, job description, and application link.
3. **Sends data to Gemini AI** for analysis.
4. **Formats & sends results to Slack**.
5. **Runs daily at 5:00 AM** using `schedule`.

## 🔄 Deployment
To deploy this on a cloud server (e.g., **Render, AWS, or DigitalOcean**), ensure:
- The Python environment is set up.
- The script runs as a background process (e.g., using `cron` or a **PM2 process manager**).

## 🛠️ Customization
- Modify `MAX_JOBS` in the script to control the number of jobs fetched.
- Adjust `schedule.every().day.at("05:00")` to change execution time.
- Update the `BASE_URL` if Talent Hub Solutions changes its website structure.

## 🐛 Troubleshooting
| Issue | Solution |
|--------|------------|
| `GEMINI_API_KEY is missing` | Check `.env` and ensure the key is set |
| `Failed to fetch job listings` | Verify the website URL and structure |
| `Slack message not sent` | Check the bot's permission in Slack |

## 📜 License
This project is **MIT licensed**.

## 🤝 Contributions
Feel free to **fork**, **modify**, and **create PRs**!

---

🎯 **Author**: Sai Prakash Sunkari
🔗 **GitHub**: [SaiPrakash-voldemort](https://github.com/SaiPrakash-voldemort)

