""" One way synchronizer for dropbox. """

import os
import pickle
import logging
from dropbox import client, auth

class Synchronizer(object):
    """ One way synchronizer for dropbox. """
    def __init__(self, config_file):
        config = auth.Authenticator.load_config(config_file)
        dba = auth.Authenticator(config)
        access_token = dba.obtain_trusted_access_token(
            config['testing_user'],
            config['testing_password'])

        self.dbc = client.DropboxClient(
            config['server'], config['content_server'],
            80, dba, access_token)
        self.root = config['root']

        self.localbox = config['localbox']
        self.datafile = config['datafile']

        logging.basicConfig(
            filename=config['logfile'],
            format='%(asctime)s:%(levelname)s:%(message)s',
            datefmt='%d.%m.%Y %H:%M:%S',
            level=logging.DEBUG)

    def get_metadata_from_server(self):
        """ Get metadata of root directory from dropbox. """

        def get_metadata(path):
            """ Get directory metadata from dropbox. """
            resp = self.dbc.metadata(self.root, path)

            if resp.status == 200:
                if resp.data['is_dir']:
                    data[resp.data['path']] = resp.data
                    for f in resp.data['contents']:
                        get_metadata(f['path'])

        data = {}
        get_metadata('/')
        return data

    def dump_metadata_to_disk(self, data):
        """ Dump all metadata to disk. """
        f = open(self.datafile, 'w')
        try:
            pickle.dump(data, f)
        except IOError:
            logging.error("Writing data failed")
        finally:
            f.close()

    def get_metadata_from_disk(self):
        """ Load all metadata to disk. """
        try:
            f = open(self.datafile, 'r')
            try:
                result = pickle.load(f)
            finally:
                f.close()
        except IOError:
            return {}
        return result

    def sync(self):
        """ Dummy realization. """
        client_data = self.get_metadata_from_disk()
        server_data = self.get_metadata_from_server()

        new_dirs = list(
            set(get_all_metafiles(server_data, is_dir=True)) -
            set(get_all_metafiles(client_data, is_dir=True)))
        new_files = list(
            set(get_all_metafiles(server_data)) -
            set(get_all_metafiles(client_data)))

        self.create_dirs(new_dirs)
        self.download_new_files(new_files)
        self.dump_metadata_to_disk(server_data)

    def create_dirs(self, new_dirs):
        """ Create new directoies in localbox. """
        create_local_dir(self.localbox)
        for path in sorted([x['path'] for x in new_dirs]):
            create_local_dir(self.localbox + path)
            logging.info("Created:" + path)

    def download_new_files(self, new_files):
        """ Download new files to localbox. """
        for path in sorted([x['path'] for x in new_files]):
            self.download_file(path)
            logging.info("Downloaded:" + path)

    def download_file(self, path):
        """ Download file from server to local path. """
        resp = self.dbc.get_file(self.root, path)
        if resp.status == 200:
            try:
                f = open(self.localbox + path, 'w')
                try:
                    f.write(resp.read())
                finally:
                    f.close()
            except IOError:
                logging.error("Writing file `%s` failed" % path)

    def is_actual(self, path, localhash):
        """ Returns False if local directory is out off date, else True. """
        return self.dbc.metadata(self.root, path, hash=localhash).status == 304


class HashDict(dict):
    """ Hashable dictionary. """
    def __key(self):
        """ Override __key(). """
        return tuple((k, self[k]) for k in sorted(self))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __setstate__(self, objstate):
        for k, v in objstate.items():
            dict.__setitem__(self, k, v)

    def __reduce__(self):
        return (HashDict, (), dict(self), )

def create_local_dir(dirname):
    """ Create dir in local drive. """
    if not os.path.isdir(os.path.join(os.getcwd(), dirname)):
        os.makedirs(os.path.join(os.getcwd(), dirname))

def get_all_metafiles(data, is_dir=False):
    """ Get list of files of directories from metadata. """
    for directory in data.itervalues():
        for f in directory['contents']:
            if f['is_dir'] == is_dir:
                yield HashDict(f)
