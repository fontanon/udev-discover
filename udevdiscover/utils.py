# -*- coding: utf-8 -*-
# vim: ts=4 
###
#
# Copyright (c) 2010 J. Félix Ontañón
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors : J. Félix Ontañón <fontanon@emergya.es>
# 
###

import exceptions
import types
import gconf

class GConfKeysDict(dict):
    VALID_KEY_TYPES = (bool, str, int, float, list, tuple, set)
    
    def __init__(self, *args, **kwargs):
        super(dict, self).__init__(*args, **kwargs)
    
    def __setitem__(self, key, val):
        if not type(val) in self.VALID_KEY_TYPES:
            raise GConfKeysDictError, 'Invalid %s for gconf key' % type(val)
        else:
            dict.__setitem__(self, key, val)

class GConfKeysDictError(exceptions.Exception):
    pass

# Partially based on http://crysol.org/node/758
class GConfStore(object):
    defaults = {}

    def __init__(self, key):
        if key.endswith('/'):
            raise GConfStoreError, "Bad directory name %s: May not end with slash '/'" % key
            return None

        self.__app_key = key
        self.__client = gconf.client_get_default()
        
        self.options = GConfKeysDict()
        self.options.update(self.defaults)

    def loadconf(self, only_defaults=False): 
        casts = {gconf.VALUE_BOOL:   gconf.Value.get_bool,
            gconf.VALUE_INT:    gconf.Value.get_int,
            gconf.VALUE_FLOAT:  gconf.Value.get_float,
            gconf.VALUE_STRING: gconf.Value.get_string,
            gconf.VALUE_LIST:   gconf.Value.get_list}

        if only_defaults:
            #FIXME: Why appears this message in stderr?
            #GConf-WARNING **: haven't implemented getting a specific locale in GConfClient
            key_iterator = [self.__client.get_entry(self.__app_key + '/' + key, 
            '', False) for key in self.defaults.keys()]
        else:
             key_iterator = self.__client.all_entries(self.__app_key)
        
        for entry in key_iterator:
            if entry is None:
                continue
                
            gval = self.__client.get(entry.key)
            if gval == None: continue
            
            if gval.type == gconf.VALUE_LIST:
                string_list = [item.get_string() for item in gval.get_list()]
                self.options[entry.key.split('/')[-1]] = string_list
            else:
                self.options[entry.key.split('/')[-1]] = casts[gval.type](gval)
 
    def saveconf(self):
        casts = {types.BooleanType: gconf.Client.set_bool,
            types.IntType:     gconf.Client.set_int,
            types.FloatType:   gconf.Client.set_float,
            types.StringType:  gconf.Client.set_string,
            types.ListType:    gconf.Client.set_list,
            types.TupleType:   gconf.Client.set_list,
            set:               gconf.Client.set_list}

        #TODO: To clear the gconf dir before save, is it convenient?
        for name, value in self.options.items():
            if type(value) in (list, tuple, set):
                string_value = [str(item) for item in value]
                casts[type(value)](self.__client, self.__app_key + '/' + name,
                    gconf.VALUE_STRING, string_value)
            else:
                casts[type(value)](self.__client, self.__app_key + '/' + name, 
                    value)

class GConfStoreError(exceptions.Exception):
    pass

class memoized(object):
   """Decorator that caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned, and
   not re-evaluated.
   """
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      try:
         return self.cache[args]
      except KeyError:
         value = self.func(*args)
         self.cache[args] = value
         return value
      except TypeError:
         # uncachable -- for instance, passing a list as an argument.
         # Better to not cache than to blow up entirely.
         return self.func(*args)
   def __repr__(self):
      """Return the function's docstring."""
      return self.func.__doc__
   def __get__(self, obj, objtype):
      """Support instance methods."""
      return functools.partial(self.__call__, obj)

import logging

class TextBufferHandler(logging.StreamHandler):
    def __init__(self, textbuffer):
        logging.StreamHandler.__init__(self)
        self.textbuffer = textbuffer

    def emit(self, record):
        logging.StreamHandler.emit(self, record)

        self.textbuffer.insert(self.textbuffer.get_end_iter(), 
            self.formatter.format(record)+'\n')

        self.textbuffer.place_cursor(self.textbuffer.get_end_iter())
