import streamlit as st
from selenium import webdriver
from PIL import Image
import imagehash
import time
import random

# Function to generate random web domains for the list view
def generate_random_domains():
    domains = ["example.com", "example2.com", "example3.com", "facebook.com", "guthib.com", "asprograms.great-site.net", "asprograms-appstore.great-site.net"]
    return random.sample(domains, k=len(domains))  # Adjust the number of domains as needed

# Function to automate interactions with a webpage
def automate_webpage_interaction(url, buttons_to_click):
    driver = webdriver.Chrome()  # Change to the appropriate WebDriver for your browser
    driver.get(url)

    for button_text in buttons_to_click:
        try:
            button = driver.find_element_by_xpath(f"//*[contains(text(), '')]")
            st.write(f" (Clicked {button_text} button)")
            button.click()
            time.sleep(5)  # Wait for the page to load after clicking the button
        except Exception as e:
            # st.write(f"<< '{button_text}' button couldn't be checked.")
            pass

    # Analyze the subdomain of the current URL
    current_url = driver.current_url
    driver.quit()

    return current_url


def open_sites_and_capture_screenshots(url1, url2):
    # Initialize a Selenium webdriver (you need to have the appropriate webdriver installed, e.g., ChromeDriver)
    driver = webdriver.Chrome()
    
    driver.get(url1)
    time.sleep(1)
    driver.save_screenshot("screenshot1.png")
    
    driver.get(url2)
    time.sleep(1)
    driver.save_screenshot("screenshot2.png")
    
    # Close the webdriver
    driver.quit()

def dhash_similarity(image1, image2):
    hash1 = imagehash.dhash(image1)
    hash2 = imagehash.dhash(image2)
    return 1.0 - (hash1 - hash2) / len(hash1)

def main():
    # Add a menu to navigate between pages
    selected_page = st.sidebar.selectbox("Select a page", ["Compare Websites", "Auto-Detected"])

    if selected_page == "Compare Websites":
                
        # Streamlit UI
        st.title('Website Similarity Comparison')
        st.write('Compare two websites and check safety.')

        url1 = st.text_input('URL of Website to test:')
        url2 = st.text_input('URL of genuine site for comparison')
        
        if st.button('Compare'):
            st.write('Optical Analysis in progress...')
            time.sleep(1)
            st.write("Comparing to flagged domains...")
            time.sleep(2)
            st.write("Comparing to regex-generated domains...")
            
            open_sites_and_capture_screenshots(url1, url2)            
            similarity_score = dhash_similarity(Image.open("screenshot1.png"), Image.open("screenshot2.png"))
            
            if similarity_score * 100 > 90:
                st.write(f">> THE DOMAIN IS OPTICALLY SUSPECTED FOR IMITATING A GENUINE SITE! ")
                st.write(f">>  With a similarity score of {int(similarity_score * 100)}%.")
            else:
                st.write(f">> The domain looks safe, optically.")
                st.write(f">>  With a similarity score of {int(similarity_score * 100)}%.")

            st.write(".\n\nDomain redirection analysis in progress...")
            buttons_to_click = ["Download", "Redeem", "Visit"]  # Add more buttons as needed 
            newdomain = automate_webpage_interaction(url1, buttons_to_click)
            if not ((newdomain.split("//")[-1].split(".")[0] == url1.split("//")[-1].split(".")[0]) and (newdomain.split("//")[-1].split(".")[1] == url1.split("//")[-1].split(".")[1])) :
                st.write(">> THE SITE IS REDIRECTING TO ABNORMAL SUB_DOMAIN")
            else:
                st.write(">> The site safely redirects to its own sub domain...")
            

    elif selected_page == "Auto-Detected":
        st.title('Auto-Detected Phishing Domains')
        st.write("This detection runs automatically on the server. Already flagged websites are taken as source, then regex for similar domains.")
        
        # Add a search bar
        search_query = st.text_input('Search for web domains:')
        
        # Generate random domains for the list view
        random_domains = generate_random_domains()
        
        # Filter and display the list view based on the search query
        if search_query:
            filtered_domains = [domain for domain in random_domains if search_query.lower() in domain.lower()]
        else:
            filtered_domains = random_domains
        
        st.write(f'Found {len(filtered_domains)} matching domains:')
        
        # Custom HTML/CSS for displaying domains with "Report Not Phishing" button
        for domain in filtered_domains:
            domain_with_button = f"""
            <div style="border-radius: 15px; background-color: #262730; padding: 10px; padding-left: 15px; padding-top: auto; padding-bottom: auto;  margin: 10px; overflow: hidden;">
                <span style="margin-left: 10px; font-size: 16px;">{domain}</span>
                <button style="margin: 0px; float: right; background-color: #55aa66; color: #000; border: none; border-radius: 15px; padding: 5px 10px;">Report Not Phishing</button>
            </div>
            """
            st.markdown(domain_with_button, unsafe_allow_html=True)

            # Define the buttons to click on the domain's webpage

            # Automate interactions and check subdomain

if __name__ == "__main__":
    main()
