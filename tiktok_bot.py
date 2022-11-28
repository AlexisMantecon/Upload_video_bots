import time, requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from random import shuffle

class tiktok:

    def upload_video(video, title, related_hashtag_keyword, profile="Default"):
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("user-data-dir=C:\\Users\\AlexisMantecon\\AppData\\Local\\Google\\Chrome Beta\\User Data")
        options.add_argument(r'--profile-directory=' + profile)
        options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
        bot = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)

        bot.get("https://www.tiktok.com/upload?lang=en")
        time.sleep(3)

        # Switching to iframe
        bot.switch_to.frame(bot.find_element(By.TAG_NAME, 'iframe'))
        
        # Setting a caption
        while True:
            try:
                caption = title + tiktok.get_RelatedHashtags(related_hashtag_keyword, (145 - len(title)))
                caption_input = bot.find_element(By.XPATH, '//div[contains(@class, "notranslate public-DraftEditor-content")]')
                caption_input.send_keys(caption)
                break
            except Exception as e:
                print("Unable to locate caption field, trying again ... \n {}".format(e))
            finally:
                time.sleep(5)
        
        # Setting video path to be upload
        while True:
            try:
                file_input = bot.find_element(By.XPATH, '//input[contains(@accept, "video")]')
                file_input.send_keys(video)
                break
            except:
                print("Unable to locate video file input, trying again ...")
            finally:
                time.sleep(5)

        # Make sure video is uploaded
        while True:
            try:
                video_uploaded = bot.find_element(By.XPATH, '//video[contains(@class, "player")]')
                break
            except:
                print('video uploading...')
            finally:
                time.sleep(5)

        # Clicking post button
        while True:
            try:
                post_button = bot.find_element(By.XPATH, '//div[contains(@class, "btn-post")]/button')
                post_button.click()
                break
            except:
                print("Unable to locate post button, trying again ...")
            finally:
                time.sleep(30)

    def get_RelatedHashtags(keyword, char_limit):
        r = requests.get("https://tiktokhashtags.com/hashtag/" + keyword + "/")
        c = r.content

        soup = BeautifulSoup(c, "html.parser")
        table = soup.find_all("table")
        rows = table[0].find_all("tr")
        data = []
        for row in rows:  
            data.append([cell.text.replace("\n", "").replace(",", "") for cell in row.find_all("td")])
        data = data[1:]

        dir = {}
        for index, hashtag, post, views, avg_views in data:
            if int(avg_views) > 1000:
                dir[hashtag] = avg_views

        hashtags = list(dir.keys())
        shuffle(hashtags)
        
        while len(" ".join(hashtags)) > char_limit:
            hashtags = hashtags[:-1]

        return " ".join(hashtags)
