
import logging
log = logging.getLogger(__name__)


class Plugin(object):

    def __init__(self, name, plugin_config={}):
        self.name = name
        self.jobs = []
        self.module = __import__(name)
        self.register_jobs()
        self.outputs = []
        if name in plugin_config:
            log.info("Config found for: {}".format(name))
            self.module.config = plugin_config[name]

        if 'setup' in dir(self.module):
            self.module.setup()

        #plugin_config
        #self._bot = plugin_config.get('bot', None)

    def register_jobs(self):
        if 'crontable' in dir(self.module):
            for interval, function in self.module.crontable:
                self.jobs.append(Job(interval, eval("self.module."+function)))
            log.info(self.module.crontable)
            self.module.crontable = []
        else:
            self.module.crontable = []

    def do(self, function_name, data):
        if function_name in dir(self.module):
            #this makes the plugin fail with stack trace in debug mode
            try:
                eval("self.module."+function_name)(data) #, self._bot)
            except:
                log.exception("Problem in module {} {}".format(function_name, data))

        if "catch_all" in dir(self.module):
            try:
                self.module.catch_all(data)
            except:
                log.exception("problem in catch all")

    def do_jobs(self):
        for job in self.jobs:
            job.check()

    def do_output(self):
        output = []
        while True:
            if 'outputs' in dir(self.module):
                if len(self.module.outputs) > 0:
                    log.info("output from {}".format(self.module))
                    output.append(self.module.outputs.pop(0))
                else:
                    break
            else:
                self.module.outputs = []
        return output
