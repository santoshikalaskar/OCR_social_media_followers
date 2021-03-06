import cv2
import numpy as np
from PIL import Image
from pytesseract import *
import re
import sys
sys.path.append('../')
import logger_hander

class OCR_instagram:
    def __init__(self):
        """
            initialize loggers
        """
        self.logger = logger_hander.set_logger()

    def fetch_text(self, img):
        """
            get Text from input img
        """
        try:
            text_result = pytesseract.image_to_string(img)
            return text_result
        except Exception as e:
            self.logger.exception("Something went Wrong while Extracting Text {}".format(e))

    def get_acc_holder_name_text(self, img_text):
        """
            get Account holder name in text format
        """
        try:
            if (img_text.find("<") == -1):
                if (img_text.find("Followers") != -1):
                    holder_name = img_text.split("Followers")[0].strip().split("\n")[-3]
                    return holder_name
            else:
                holder_name = img_text.split("<")[1].split('\n')[0]
                regexp = "(?:^|(?<= ))[a-zA-Z0-9]+(?= |$)"
                holder_name = re.findall(regexp, holder_name)
                if len(holder_name) > 0:
                    return holder_name[0]
                else:
                    holder_name = img_text.split("<")[1].strip().split("\n")[0]
                    return holder_name
        except Exception as e:
            self.logger.exception("Something went Wrong while getting Account Holder Name {}".format(e))

    def check_followers(self, followers_list, check_list):
        """
            Check list of followers present or not from result list
        """
        try:
            result_list = []
            check_list = [x.lower() for x in check_list]
            followers_list = [x.lower() for x in followers_list]
            for check_list_item in check_list:
                if check_list_item in followers_list:
                    result_list.append(True)
                else:
                    result_list.append(False)
            return result_list
        except Exception as e:
            self.logger.exception("Something went Wrong while Checking list of followers present or not from result list {}".format(e))

    def increase_size(self, img):
        width = int(img.shape[1] * 2)
        height = int(img.shape[0] * 2)
        dim = (width, height)
        resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        self.logger.info('Resized Dimensions : {}'.format(str(resized_img.shape)))
        return resized_img

    def get_followers_list(self, text):
        if (text.find("<") == -1):
            return text
        else:
            followers_list = text.split("<")[1].split()
            return followers_list
    def instagram_handler(self, img_path, check_followers_list):
        """
           Instagram OCR
           input : img_path, social_media_name & followers_list for checking
           Output : Followers present or not Present
        """
        try:
            img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
            self.logger.info('Original Dimensions : {}'.format(str(img.shape)))
            text_result = self.fetch_text(img)

            if img.shape[1] < 600 and img.shape[0] < 1300 :
                resized_img = self.increase_size(img)
                text_result = self.fetch_text(resized_img)

            print("\n-------------------------\n",text_result, "\n---------------------------------")

            acc_holder_name = self.get_acc_holder_name_text(text_result)
            print("Account Holder Name : ",acc_holder_name)
            followers_list = self.get_followers_list(text_result)
            result = self.check_followers(followers_list, check_followers_list)
            if all(bool(x) == True for x in result):
                print("\n ******************\n All Followers Present \n ******************\n")
            else:
                print("\n ******************\n Followers not Present : ",result, "\n ******************\n")
        except Exception as e:
            self.logger.exception("Something went Wrong in instagram handler {}".format(e))


# if __name__ == "__main__":
#     ocr_obj = OCR_instagram()
# 
#     img_path = "Data/test_s3.jpg"
#     # check_followers_list = ['harshu_kitty_lover_20', 'ganeshkondawar88']
#     check_followers_list = ['_c_h_h_a_', 'a_x_a_y_2_2_2']
#     social_media_name = "instagram"
# 
#     ocr_obj.instagram_handler(img_path,social_media_name,check_followers_list)
    