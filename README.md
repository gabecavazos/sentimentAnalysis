Instagram Comment Sentiment Analysis

This project analyzes the sentiment of comments on a given Instagram post. Using a combination of web scraping, machine learning, and sentiment analysis, the program fetches comments from an Instagram post and classifies them as positive, negative, or neutral.

Features

Scrapes comments from Instagram posts using instascrape and selenium.
Outputs sentiment results in an Excel file using pandas and xlsxwriter.
Simple and interactive user interface using Streamlit.
Utilizes OpenAI’s API for advanced text sentiment processing.


Installation

Follow these steps to set up and run the project:

1. Clone the Repository
git clone https://github.com/yourusername/instagram-sentiment-analysis.git
cd instagram-sentiment-analysis
2. Install Dependencies
Install all required packages listed in requirements.txt:

pip install -r requirements.txt
The project requires the following major libraries:

selenium: For browser automation and scraping.
tensorflow and keras: For machine learning and sentiment analysis.
pandas, openpyxl, xlsxwriter: For data processing and Excel export.
instascrape: For scraping Instagram posts.
Streamlit: For building an interactive UI.
requests, datasets, numpy, xlrd: Additional utilities.
3. Set Up OpenAI API
Obtain an OpenAI API key by signing up at OpenAI.
Add your OpenAI API key to the main.py script or use an environment variable. Example:
import os
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key'
Usage

1. Run the Program
Start the application by running the main.py file:

python main.py
2. Interact with the Streamlit Interface
Open the local Streamlit app in your browser (usually at http://localhost:8501).
Provide the URL of the Instagram post you want to analyze.
Click "Fetch Comments" to scrape comments from the post.
View sentiment analysis results directly in the interface or download them as an Excel file.
Output

Sentiment Results: Displays a breakdown of the sentiment (positive, negative, neutral) for the scraped comments.
Excel File: Exports a detailed list of comments and their corresponding sentiment into an Excel file for further analysis.
Additional Notes

Instagram Authentication:
Some features of instascrape may require Instagram login. Use selenium for automated login if needed.
Ensure you comply with Instagram's scraping policies to avoid account bans.
Browser Setup for Selenium:
Ensure you have the correct web driver installed for Selenium (e.g., ChromeDriver for Google Chrome).
Place the driver in a directory included in your system's PATH or specify its location in the code.
Environment Variables:
For added security, consider storing sensitive information like the OpenAI API key in environment variables instead of hardcoding them in the script.
Troubleshooting

Dependency Issues:
If any dependencies fail to install, ensure you are using Python 3.8 or higher and have the latest version of pip.
Browser Compatibility:
Make sure your browser and Selenium driver are up-to-date and compatible.
Rate Limits:
OpenAI API and Instagram scraping may be subject to rate limits. Handle these gracefully in your code.
Contributing

Contributions are welcome! Feel free to submit pull requests or report issues.

License

This project is licensed under the MIT License.

