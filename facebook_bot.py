import time, requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from random import shuffle

class facebook:

    def upload_video(video, title, related_hashtag_keyword, page_name, profile="Default"):
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("user-data-dir=C:\\Users\\AlexisMantecon\\AppData\\Local\\Google\\Chrome Beta\\User Data")
        options.add_argument(r'--profile-directory=' + profile)
        options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
        bot = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)

        bot.get("https://www.facebook.com/" + page_name)
        time.sleep(3)
 
        # Clicking new post element
        while True:
            try:
                element = bot.find_element(By.XPATH, '//span[contains(text(), "¿Qué estás pensando?")]')
                element.click()
                break
            except:
                print("Unable to locate new post element, trying again ...")
            finally:
                time.sleep(5)

        # Clicking photo/video 
        while True:
            try:
                element = bot.find_element(By.XPATH, '//div[contains(@aria-label, "Foto/video")]')
                element.click()
                break
            except:
                print("Unable to locate photo/video element, trying again ...")
            finally:
                time.sleep(5)

        # Setting video path to be upload
        while True:
            try:
                element = bot.find_element(By.XPATH, '//form[contains(@method, "POST")]//input[contains(@accept, "video")]')
                element.send_keys(video)
                break
            except:
                print("Unable to locate video file input, trying again ...")
            finally:
                time.sleep(5)

        # Setting a caption
        while True:
            try:
                caption = title + facebook.get_RelatedHashtags(related_hashtag_keyword, 200)
                caption_input = bot.find_element(By.XPATH, '//div[contains(@aria-label, "¿Qué estás pensando?")]/p')
                caption_input.send_keys(caption)
                break
            except Exception as e:
                print("Unable to locate caption field, trying again ... \n {}".format(e))
            finally:
                time.sleep(5)

        # Clicking post button
        while True:
            try:
                post_button = bot.find_element(By.XPATH, '//span[contains(text(), "Publicar en Facebook")]')
                post_button.click()
                break
            except:
                print("Unable to locate post button, trying again ...")
            finally:
                time.sleep(30)

    def get_RelatedHashtags(keyword, char_limit):
        r = requests.get("https://best-hashtags.com/hashtag/" + keyword + "/")
        c = r.content

        soup = BeautifulSoup(c, "html.parser")

        hashtags = []
        for word in ["popular", "medium", "easy"]:
            element = soup.find_all("div", {"id":word})
            element = element[0].find_all("div",{"class":"tag-box"})
            element = element[0].find_all()
            element = element[0].text
            for hashtag in element.split(" "):
                hashtags.append(hashtag)

        hashtags = set(hashtags)
        hashtags = list(hashtags)
        shuffle(hashtags)

        while len(" ".join(hashtags)) > char_limit:
            hashtags = hashtags[:-1]

        return " ".join(hashtags)
