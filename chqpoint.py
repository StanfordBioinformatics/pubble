#!/usr/bin/env python3

import copy
import glob
import json
import os

class AnalysisConfig:

      """
      AnalysisConfig contains data provided by the user to describe the 
      layout of a results directory and metadata. Using instructions from 
      config, it can scan a directory for files that match search patterns, 
      validate file characteristics against settings in 
      AnalysisConfig.configdata, and return a data dictionary with info 
      to describe an analysis directory.
      """

      def __init__(self, analysisdir, configstr=None, configfile=None):
            if not (configstr or configfile):
                  raise Exception(
                        'Either a string or a file containing config '\
                        'info is required.')
            if configstr and configfile:
                  raise Exception(
                        'Expected either a configstr or configfile '\
                        'but received both: %s' % (configstr, configfile))

            self.analysisdir = analysisdir
            if configfile:
                  self._initfromfile(configfile)
            else: 
                  self._initfromstring(configstr)

      def _initfromfile(self, configfile):
            if not os.path.isfile(configfile):
                  raise Exception('Could not find configfile %s'
                                  % configfile)
            with open(configfile) as f:
                  configstr = f.read()
            self._initfromstring(configstr)

      def _initfromstring(self, configstr):
            try:
                  configdata = json.loads(configstr)
            except ValueError:
                  raise Exception('Config is not a valid JSON object:\n %s'
                                  % configstr)
            self.configdata = self._clean(configdata)

      def getanalysisdata(self):
            # The scan will use self.configdata generated from the config json
            # to scan the analysis directory and find inputs and outputs.

            # Data that will be discovered by the directory scan
            # or transferred from the configdata
            # to be used to register the analysis directory
            analysisdata = {
                  'application': None,
                  'metadata': None,
                  'inputs':[], 
                  'outputs': [], 
            }

            # Search for inputs and outputs with filenames 
            # that match the search string
            analysisdata['inputs'] = self._scansearchpatterns(
                  self.analysisdir, self.configdata.get('inputs'))
            analysisdata['outputs'] = self._scansearchpatterns(
                  self.analysisdir, self.configdata.get('outputs'))

            # metadata and application are copied unchanged
            analysisdata['metadata'] = copy.deepcopy(
                  self.configdata.get('metadata'))
            analysisdata['application'] = copy.deepcopy(
                  self.configdata.get('application'))
                  
            return analysisdata

      def _scansearchpatterns(self, analysisdir, configsearchpatterns):
            print(configsearchpatterns)
            SCANNERS = {
                  'file': self._scanfile, # For 'file' inputs/outputs
                  # 'chqpoint': self._scanchqpoint # For 'chqpoint' inputs
            }

            matches = []
            if configsearchpatterns:
                  for obj in configsearchpatterns:
                        type = obj.get('type')
                        name = obj.get('name')
                        if obj.get('absolutepath'):
                              searchpath = obj.get('absolutepath')
                        elif obj.get('relativepath'):
                              searchpath = os.path.join(
                                    analysisdir, obj.get('relativepath'))
                        else:
                              print(obj) 
                              raise Exception('No path found')
                        mincount = obj.get('mincount')
                        maxcount = obj.get('maxcount')
                        scanner = SCANNERS[type]
                        matches += scanner(
                              searchpath, name, mincount, maxcount)
            return matches

      def _scanfile(self, path, name, mincount, maxcount):
            # Scanning for 0 or more files that match the 
            # search string in 'path'

            filelist = []
            newpaths = glob.glob(os.path.join(path))
            for newpath in newpaths:
                  dataobj = {
                        'name': name,
                        'path': newpath,
                  }
                  filelist.append(dataobj)
            if mincount:
                  if len(filelist) < mincount:
                        raise Exception("Didn't find at least {} file(s) matching {}".format(mincount, path))
            if maxcount:
                  if len(filelist) > maxcount:
                        raise Exception("Found over {} file(s) matching {}".format(maxcount, path))
            return filelist

#      def _scanchqpoint(self, searchpattern):
            # TODO

      def _clean(self, configjson):
            # Here we verify that it follows the rules for a
            # dirmap object. We do this here rather than in the scan because
            # errors should be raised when initializing, not after
            # a long wait while scanning directories.

            # Check top-level properties
            ALLOWED_KEYS=[u'application', u'metadata', u'inputs', u'outputs']
            self._validatekeys(configjson, allowed=ALLOWED_KEYS)

            inputs = configjson.get('inputs')
            outputs = configjson.get('outputs')
            metadata = configjson.get('metadata')
            application = configjson.get('application')

            self._validateinputs(inputs)
            self._validateinputs(outputs, isoutput=True)
            self._validatemetadata(metadata)
            self._validateapplication(application)

            return configjson

      def _validateinputs(self, inputs, isoutput=False):
            if inputs:
                  for inputobj in inputs:
                        self._validateinput(inputobj, isoutput=isoutput)

      def _validateinput(self, inputobj, isoutput=False):
            if inputobj is None:
                  return
            ALLOWED_KEYS=[u'type', u'name', u'relativepath', u'absolutepath', 
                          u'maxcount', u'mincount']
            REQUIRED_KEYS=[u'name', u'type']
            EXACTLY_ONE_REQUIRED=[[u'relativepath', u'absolutepath']]
            self._validatekeys(
                  inputobj, allowed=ALLOWED_KEYS, required=REQUIRED_KEYS, 
                  exactlyone=EXACTLY_ONE_REQUIRED)

            ALLOWED_VALUES = {
                  'type': [u'file'],
                  'absolute': [True, False],
            }

            # chqpoint data type is allowed for inputs only
            if not isoutput:
                  ALLOWED_VALUES['type'].append(u'chqpoint')

            for key in ALLOWED_VALUES:
                  if inputobj.get(key):
                        self._validatevalues(key, inputobj.get(key), 
                                             ALLOWED_VALUES[key])

            ALLOWED_TYPES = {
                  'name': str,
                  'path': str,
                  'maxcount': int,
                  'mincount': int,
            }
            for key in ALLOWED_TYPES:
                  if inputobj.get(key):
                        self._validatetype(key, inputobj.get(key), 
                                           ALLOWED_TYPES[key])

            mincount = inputobj.get('mincount')
            maxcount = inputobj.get('maxcount')

            if mincount and maxcount:
                  if mincount > maxcount:
                        raise Exception(
                              'mincount %s is greater than maxcount %s' % (
                                    mincount, maxcount))
            
      def _validatemetadata(self, metadata):
            # Anything goes as long as it's a valid json.
            pass

      def _validateapplication(self, application):
            if application:
                  ALLOWED_KEYS = [u'name', u'version']
                  REQUIRED_KEYS = [u'name', u'version']
                  self._validatekeys(application, allowed=ALLOWED_KEYS, 
                                     required=REQUIRED_KEYS)

      def _validatekeys(self, configdict, allowed=[], required=[], 
                        atleastone=[], exactlyone=[]):
            for key in configdict.keys():
                  if not key in allowed:
                        raise Exception(
                              'Unrecognized key in config: %s\n'\
                              'Allowed keys: %s' % (key, allowed))
            for key in required:
                  if not key in configdict.keys():
                        raise Exception(
                              'Required key missing from config: %s\n'\
                              'Keys required: %s\n'\
                              'Keys found: %s' % (
                                          key, required, configdict.keys()))

            for keyset in atleastone:
                  if not any(map(lambda x: x in configdict.keys(), keyset)):
                        raise Exception(
                              'At least one of these keys is required: %s\n'\
                              'Keys found: %s' % (
                                          atleastone, configdict.keys())
                              )

            for keyset in exactlyone:
                  if not sum(map(lambda x: x in configdict.keys(), 
                                 keyset)) == 1:
                        raise Exception(
                              'Exactly one of these keys is required: %s\n'\
                                    'Keys found: %s' % (
                                          exactlyone, configdict.keys())
                              )

      def _validatevalues(self, key, value, allowedvalues):
            if not value in allowedvalues:
                  raise Exception(
                        'Unrecognized value in config: %s\n'\
                        'Allowed values: %s' % (key, allowedvalues))

      def _validatetype(self, key, value, requiredtype):
            if not isinstance(value, requiredtype):
                  raise Exception(
                        'Unexpected type for %s. Expected %s but found %s' \
                        % (key, requiredtype, type(value)))

class Analysis:

#      CHQPOINTFILENAME = 'metadata.json'

      def __init__(self, analysisdata):
            self.setanalysisdata(analysisdata)

      def setanalysisdata(self, analysisdata):
            self.validateanalysisdata(analysisdata)
            self.analysisdata = analysisdata

      def validateanalysisdata(self, analysisdata):
            self.validateserializable(analysisdata)
            # TODO validate schema

      @classmethod
      def new(cls, path, configstr=None, configfile=None):
            config = AnalysisConfig(path, configstr=configstr, 
                                    configfile=configfile)
            analysisdata = config.getanalysisdata()
            return cls(analysisdata)

      def getoutputs(self):
            return self.analysisdata.get('outputs')

      def getoutput(self, outputname):
            outputs = []
            for output in self.getoutputs():
                  if output.get('name') == outputname:
                        outputs.append(output['path'])
            return outputs

      def getmetadata(self):
            return self.analysisdata.get('metadata')

      def validateserializable(self, data):
            try:
                  json.dumps(data)
            except TypeError:
                  raise Exception('Object is not serializable: %s' % data)

            

#      @classmethod
#      def register(cls, analysisdir, configstr=None, configfile=None):
#            config = ChqpointConfig(analysisdir, configstr=configstr, configfile=configfile)
#            chqpointdata = config.scananalysisdir(analysisdir)
#            cls._savedata(chqpointdata)

#      def save(self):
#            pass
            # TODO
      
#      @classmethod
#      def _savedata(cls, chqpointdata):
#            import pdb; pdb.set_trace()
            # 'Application', 'ApplicationInstance', 'ApplicationInstanceHasInputDataObject', 'ApplicationInstanceHasOutputDataObject'

            # Look up application, error if it does not exist
#            if chqpointdata.get('application'):
#                  name = chqpointdata.get('application').get('name')
#                  version = chqpointdata.get('application').get('version')
#                  try:
#                        appliction = models.Application.select().where(models.Application.name == name & models.Application.version == version).get()
#                  except models.Application.DoesNotExist:
#                        raise Exception('Could not find application named "%s" with version "%s"' % (name, version))
#            else:
#                  application = None
#
#            metadata = json.dumps(chqpointdata.get('metadata')) # may be null

#            models.ApplicationInstance(metadata=metadata, application=application)

      #      if chqpointdata.get('inputs'):
                  
                                                            

            # Write to database objects
            # save
            # Write uuid to file

#      @classmethod
#      def _getchqpointfile(cls, rootdir):
#            return os.path.join(rootdir, CHQPOINTFILENAME)

