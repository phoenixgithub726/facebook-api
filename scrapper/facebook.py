from bs4 import BeautifulSoup
import mysql.connector
import json

from utils.setting import setting
_facebook = None
class FaceBook:
    @staticmethod
    def getInstance():
        global _facebook
        if _facebook == None:
            _facebook = FaceBook()
        return _facebook

    def __init__(self):
        db_host = setting.getInstance().get('MYSQL_HOST')
        db_user = setting.getInstance().get('MYSQL_USER')
        db_pass = setting.getInstance().get('MYSQL_PASS')
        db_name = setting.getInstance().get('MYSQL_DB')
       
        self.db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name
        )

    # save json data into mysql
    def save(self, data={}):
        try:
            mycursor = self.db.cursor()
            sql = "INSERT INTO pages (json) VALUES (%s)"
            val = (json.dumps(data),)
            mycursor.execute(sql, val)
            self.db.commit()
            return True
        except mysql.connector.Error as err:
            print("Database Connection Error: {}".format(err))
            return err
    def callFunc(self, type='', params=[]):
        actions = { 
            'Person': self.local_person, 
            'LocalBusiness': self.local_business, 
        } 
        func = actions.get(type)
        return func(params)

    def parse(self):
        with open("element/ruman.html", encoding="utf-8") as f:
            data = f.read()
            soup = BeautifulSoup(data, 'html.parser')
            print(type(soup))
            utype = soup.find_all("script",type="application/ld+json")

            if len(utype) > 0:
                utype = json.loads(utype[0].string)
                # print(utype['@type'])
                info = self.callFunc(utype['@type'], soup)
            
            print(info)
            mail_address = ""
            mail_tag = soup.select('a[href^= mailto]')
            if len(mail_tag) > 0:
                for mail in mail_tag:
                    mail_address += mail.text
            mail_address = mail_address.strip()
            print('mail_address', mail_address)

            info['mail']= mail_address      
            
            if self.save(info) == True:
                return info
            else:
                return "Database Connection Error: {}".format(err)

    def local_business(self, soup):
        div_profile = soup.select('div[id^=PagesProfileAboutInfoPagelet_]')

        # find the PagesProfileAboutInfoPagelet_ div
        if len(div_profile) > 0:
            for div in div_profile:
                # div_profile_children = div.findChildren('div', recursive=True)
                div_profile_children = div.find_all('div', recursive=False)

        if len(div_profile_children) > 0:
            print("length of profile",len(div_profile_children))
            div_find_us = div_profile_children[1]
            return (self.find_us(div_find_us))
            # print(div_find_us)
            div_business_info = div_profile_children[2]
        
    def local_person(self, soup):
        print('person')
      

    def find_us(self, section_find_us=''):
        div_find_us = section_find_us.findChildren('div',recursive=False)[0].findChildren('div',recursive=False)[0].findChildren('div', recursive=False)[0].findChildren('div', recursive=False)
       
        #FIND US div div_find_us[0]
        div_title = div_find_us[0].find('span')
        # if div_title.text == "FIND US":
        #     print("find us")
                
        # Address Div div_find_us[1]
        div_address = div_find_us[1].findChildren('div',recursive=False)
        full_address = ""
        for address in div_address[1].find_all('div'):
            full_address += address.text + "  "
            full_address = full_address.strip()

        # Phone Div div_find_us[3]
        call_phone = ""
        for phone in div_find_us[3].findChildren('div', recursive=False):
            call_phone += phone.text
        call_phone = call_phone.strip()
        return {"phone": call_phone, "address":full_address}