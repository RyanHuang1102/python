import ConfigParser

class config():
    def __init__(self, file_path):
        self.parser = ConfigParser.SafeConfigParser()
        self.path = file_path
        if (self.parser.read(self.path) == []):
            open(self.path,'wb').close()
    def setcfg(self, section, field, value):
        try:
            self.parser.add_section(section)
        except:
            pass
        finally:
            self.parser.set(section, field, value)
            self.parser.write(open(self.path,'wb'))
            return 0
    def getcfg(self, section, field):
        try:
            return self.parser.get(section, field)
        except:
            print "check section or field name"
            return -1
    def rmcfg(self, section):
        self.parser.remove_section(section)
        self.parser.write(open(self.path,'wb'))
        return 0
