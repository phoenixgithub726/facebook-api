import os
import json

_setting = None
class setting:
    settings = {}
    @staticmethod
    def getInstance():
        # singletone class's get instance static method.
        global _setting
        if _setting == None:
            _setting = setting()
        return _setting

    def __init__(self):
        self.loadsettings()

    def loadsettings(self):
        self.ROOT_DIR = '{0}/..'.format(os.path.dirname(os.path.abspath(__file__)))
        try:
            # load settings from setting.json. It should be called one time at first.
            settingsPath ='%s/settings.json' % self.ROOT_DIR
            f = open(settingsPath, 'r')
            js_data = f.read()
            parsed = json.loads(js_data)
            self.settings = parsed

            # make log path from local to full.
            self.settings['MYSQL_HOST'] = parsed.get('MYSQL_HOST')
            self.settings['MYSQL_USER'] = parsed.get('MYSQL_USER')
            self.settings['MYSQL_PASS'] = parsed.get('MYSQL_PASS')
            self.settings['MYSQL_DB'] = parsed.get('MYSQL_DB')
            
           
            # make chrome driver path from local to full.
            self.settings['CHROMEDRIVER'] = self.ROOT_DIR + parsed.get('CHROMEDRIVER')
           
            # if the log folder does not exist, create it.
            if os.path.isdir(self.settings['LOG_PATH']) == False:
                os.mkdir(self.settings['LOG_PATH'])

        except Exception as e:
            print('Load settings error. Run using default settings. Details: %s' % str(e))
            return False

        return True

    def get(self, field=''):
        val = self.settings.get(field, '')
        if val == None:
            print('Get settings error. There is no value for %s' % field)
        return val