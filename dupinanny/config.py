#!/usr/bin/env python

##########################################################################
#    dupinanny backup scripts for duplicity
#    Copyright (C) 2008 Timothee Besset
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################

import os, re, sys

from optparse import OptionParser

class ConfigBase:
    def __init__(self, dupi):
        self.dupi = dupi
        self.config = dupi['config']
        
        self.lockfile = self.config['lockfile']
        
        # NOTE: may get an override from command line
        self.dry_run = False
        try:
            self.dry_run = self.config['dry_run']
        except:
            pass

        self.item = None

        self.duplicity = 'duplicity'
        try:
            self.duplicity = self.config['duplicity']
        except:
            pass

        self.remove_older = 4
        try:
            self.remove_older = self.config['remove_older']
        except:
            pass        

    def commandLineOverrides(self, options):
        if (options.dry_run):
            self.dry_run = options.dry_run

        self.cleanup = options.cleanup
        if (self.cleanup):
            self.dry_run = True

        self.force_remove_older = False
        if (not options.remove_older is None):
            self.remove_older = options.remove_older
            print ('*** command line override for remove_older: %d ***' % 
                self.remove_older)
            self.force_remove_older = True
            self.dry_run = True

        if (self.dry_run):
            print '*** running in test mode ***'

        self.full = options.full
        if (self.full):
            print '*** FLAGING FULL BACKUP ***'

        if (options.item):
            self.item = options.item

def readConfig(cmdargs):

    parser = OptionParser()
    parser.add_option('--dry-run', action='store_true', dest='dry_run', 
        help='show commands, do not execute except collection-status')
    parser.add_option('--cleanup', action='store_true', dest='cleanup', 
        help = 'cleanup only, implies --dry-run')
    parser.add_option('--remove-older', action='store', type='int', 
        dest='remove_older', default=None, help='run remove_old only, with the '
        'given value. implies --dry-run (set the value in the config to '
        'customize for each run and do other operations)')
    parser.add_option('--config', action='store', type='string', 
        dest='configFile', default='config.cfg.example', 
        help='use this config file')
    parser.add_option('--full', action='store_true', dest='full', help='force '
        'a full backup. will retry for each backup target if necessary until '
        'full backups are done')
    parser.add_option('--list', action='store_true', dest='list',
        help='show the list of available backups targets')
    parser.add_option('--item', action='store', type='string',
        dest='item', default=None, help='backup item to execute. Leave '
        'to backup all items.')
    (options, args) = parser.parse_args(cmdargs)
    
    globals = {}
    locals = {}
    try:
        execfile(options.configFile, globals, locals)
    except:
        print ('exception raised while reading config file %s' % 
            options.configFile)
        raise
    if (not locals.has_key('DupiConfig')):
        raise 'DupiConfig dictionary was not defined'
    DupiConfig = locals['DupiConfig']
    
    if options.list:
        attrsname = {
            'name': 'Item', 
            'type': 'Type',
            'root': 'Path', 
            'destination': 'Destination',
            }
        maxattrs = {}
        for attr in ['name', 'type', 'root', 'destination']:
            maxattrs[attr] = max([len(getattr(x, attr)) for x in 
                    DupiConfig['items']])
            maxattrs[attr] = max(maxattrs[attr], len(attrsname[attr]))
        print '%s   %s   %s   %s' % (
            attrsname['name'].ljust(maxattrs['name']),
            attrsname['type'].ljust(maxattrs['type']), 
            attrsname['root'].ljust(maxattrs['root']), 
            attrsname['destination'].ljust(maxattrs['destination']),
            )
        print '%s   %s   %s   %s' % (
            '-' * maxattrs['name'],
            '-' * maxattrs['type'],
            '-' * maxattrs['root'],
            '-' * maxattrs['destination'],
            )
        for item in DupiConfig['items']:
            print '%s   %s   %s   %s' % (
                item.name.ljust(maxattrs['name']),
                item.type.ljust(maxattrs['type']),
                item.root.ljust(maxattrs['root']), 
                item.destination.ljust(maxattrs['destination']),
                )
        sys.exit(0)
    
    # setup default backup class if needed
    if (not DupiConfig.has_key('backup')):
        from dupinanny import Backup
        DupiConfig['backup'] = Backup(DupiConfig)

    DupiConfig['backup'].commandLineOverrides(options)
    
    return DupiConfig

if __name__ == '__main__':
    readConfig()

