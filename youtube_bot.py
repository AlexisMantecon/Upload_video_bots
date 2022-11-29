import time
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from random import shuffle


class youtube:
    def __init__(self):
        pass

    def upload_video(self, video, title, related_hashtag_keyword, profile="Default"):
        """
        Use example:

        from youtube_bot import youtube

        obj = youtube()
        obj.upload_video(video=r'C:\myvideo.mp4',
                            title="Tutorial #shorts ",
                            related_hashtag_keyword="fyp",
                            profile="Default")
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument(
            "user-data-dir=C:\\Users\\AlexisMantecon\\AppData\\Local\\Google\\Chrome Beta\\User Data")
        options.add_argument(r'--profile-directory=' + profile)
        options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
        bot = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(), chrome_options=options)

        bot.get("https://studio.youtube.com")
        time.sleep(3)

        # Clicking upload button
        while True:
            try:
                upload_button = bot.find_element(
                    By.XPATH, '//*[@id="upload-icon"]')
                upload_button.click()
                break
            except:
                print("Unable to locate upload button, trying again ...")
            finally:
                time.sleep(5)

        # Setting video path to be upload
        while True:
            try:
                file_input = bot.find_element(
                    By.XPATH, '//*[@id="content"]/input')
                file_input.send_keys(video)
                break
            except:
                print("Unable to locate video file input, trying again ...")
            finally:
                time.sleep(5)

        # Setting a caption
        while True:
            try:
                caption = title + \
                    self.get_RelatedHashtags(
                        related_hashtag_keyword, (90 - len(title)))
                caption_input = bot.find_element(
                    By.XPATH, '//div[contains(@aria-label, "Agrega un título")]')
                caption_input.send_keys(caption)
                break
            except Exception as e:
                print("Unable to locate title field, trying again ... \n {}".format(e))
            finally:
                time.sleep(5)

        # Adding hashtags
        while True:
            try:
                desc = "\n\n" + \
                    self.get_RelatedHashtags(related_hashtag_keyword, 4500)
                desc_input = bot.find_element(
                    By.XPATH, '//div[contains(@aria-label, "Cuéntales a los usuarios sobre el video")]')
                desc_input.send_keys(desc)
                break
            except Exception as e:
                print("Unable to locate desc field, trying again ... \n {}".format(e))
            finally:
                time.sleep(5)

        # Clicking next button 3 times
        while True:
            try:
                next_button = bot.find_element(
                    By.XPATH, '//*[@id="next-button"]')
                for i in range(3):
                    next_button.click()
                    time.sleep(3)
                break
            except:
                print(
                    "Unable to locate next button {i}, trying again ...".format(i))
            finally:
                time.sleep(5)

        # Clicking post button
        while True:
            try:
                post_button = bot.find_element(
                    By.XPATH, '//*[@id="done-button"]')
                post_button.click()
                break
            except:
                print("Unable to locate post button, trying again ...")
            finally:
                time.sleep(30)
        bot.quit()

    def get_RelatedHashtags(self, keyword, char_limit):
        try:
            r = requests.get(
                "https://best-hashtags.com/hashtag/" + keyword + "/")
            c = r.content

            soup = BeautifulSoup(c, "html.parser")

            hashtags = []
            for word in ["popular", "medium", "easy"]:
                try:
                    print("Looking for " + word + " hashtags ...")
                    element = soup.find_all("div", {"id": word})
                    element = element[0].find_all("div", {"class": "tag-box"})
                    element = element[0].find_all()
                    element = element[0].text
                    for hashtag in element.split(" "):
                        hashtags.append(hashtag)
                except:
                    next

            hashtags = set(hashtags)
            hashtags = list(hashtags)
            shuffle(hashtags)

            while len(" ".join(hashtags)) > char_limit:
                hashtags = hashtags[:-1]

            return " ".join(hashtags)
        except Exception as e:
            print("Unable to get hashtags ... \n {}".format(e))
            return "#NoHuboHashtagsCompa"
