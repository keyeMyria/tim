import ConfigParser

class StartupConfig:

      def __init__(self):
          self.config = ConfigParser.ConfigParser()

      def config_read(self):
	  try:
             self.config.read("/srv/oneiros/oneiros/local/lib/python2.7/site-packages/oneiros/dummy_config.ini")
	     return self.config.sections()
	  except Exception as error:
	     return error

      def bots(self):
    	  installed = {}
	  section = self.config_read()
          options = self.config.options(section[0])
          for option in options:
	      try:
		 installed[option] = self.config.get(section[0], option).replace(" ","").split(",")
		 if installed[option] == -1:
		    print("skip: %s" % option)
	      except:
		 print("exception on %s!" % bot)
          return installed

#conf = StartupConfig()
#print conf.bots()
