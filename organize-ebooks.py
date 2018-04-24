import ipdb
import ast
from configparser import ConfigParser, NoOptionError, NoSectionError
import linecache
import os
import sys

from lib import search_file_for_isbns


# Environment variables
SETTINGS_PATH = os.path.expanduser('~/PycharmProjects/digital_library/config.ini')


# TODO: add function in utilities
def print_exception(error=None):
    """
    For a given exception, PRINTS filename, line number, the line itself, and
    exception description.

    ref.: https://stackoverflow.com/a/20264059

    :return: None
    """
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    if error is None:
        err_desc = exc_obj
    else:
        err_desc = "{}: {}".format(error, exc_obj)
    # TODO: find a way to add the error description (e.g. AttributeError) without
    # having to provide the error description as input to the function
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), err_desc))


# TODO: add function in utilities
def get_data_type(val):
    """
    Given a string, returns its corresponding data type

    ref.: https://stackoverflow.com/a/10261229

    :param val: string value
    :return: Data type of string value
    """
    try:
        # TODO: not safe to evaluate string
        t = ast.literal_eval(val)
    except ValueError:
        return str
    except SyntaxError:
        return str
    else:
        if type(t) is bool:
            return bool
        elif type(t) is int:
            return int
        elif type(t) is float:
            return float
        else:
            return str


# TODO: add function in utilities
def get_option_value(parser, section, option):
    value_type = get_data_type(parser.get(section, option))
    try:
        if value_type == int:
            return parser.getint(section, option)
        elif value_type == float:
            return parser.getfloat(section, option)
        elif value_type == bool:
            return parser.getboolean(section, option)
        else:
            return parser.get(section, option)
    except NoSectionError:
        print_exception()
        return None
    except NoOptionError:
        print_exception()
        return None


# TODO: add function in utilities
def read_config(config_path):
    parser = ConfigParser()
    found = parser.read(config_path)
    if config_path not in found:
        print("ERROR: {} is empty".format(config_path))
        return None
    options = {}
    for section in parser.sections():
        options.setdefault(section, {})
        for option in parser.options(section):
            options[section].setdefault(option, None)
            value = get_option_value(parser, section, option)
            if value is None:
                print("ERROR: The option '{}' could not be retrieved from {}".format(option, config_path))
                return None
            options[section][option] = value
    return options


def check_file_for_corruption():
    return ''


def skip_file(file_path, reason):
    raise NotImplementedError('skip_file is not implemented!')


# Arguments: path, reason (optional)
def organize_by_filename_and_meta(file_path, reason=''):
    raise NotImplementedError('organize_by_filename_and_meta is not implemented!')


def organize_by_isbns(file_path, isbns):
    pass


def organize_file(file_path, corruption_check_only=False, organize_without_isbn=False):
    ipdb.set_trace()
    file_err = check_file_for_corruption()
    if file_err:
        # TODO: decho
        print('File {} is corrupt with error {}'.format(file_path, file_err))
    elif corruption_check_only:
        # TODO: decho
        print('We are only checking for corruption, do not continue organising...')
        skip_file(file_path, 'File appears OK')
    else:
        # TODO: decho
        print('File passed the corruption test, looking for ISBNs...')
        isbns = search_file_for_isbns(file_path)
        if isbns:
            print('Organizing {} by ISBNs {}!'.format(file_path, isbns))
            organize_by_isbns(file_path, isbns)
        elif organize_without_isbn:
            print('No ISBNs found for {}, organizing by filename and metadata...'.format(file_path))
            organize_by_filename_and_meta(file_path, 'No ISBNs found')
        else:
            skip_file(file_path, 'No ISBNs found; Non-ISBN organization disabled')
    # TODO: decho
    print('=====================================================')


if __name__ == '__main__':
    # Read configuration file
    config_ini = read_config(SETTINGS_PATH)
    if config_ini is None:
        # TODO: exit script
        print("ERROR: {} could not be read".format(SETTINGS_PATH))

    # f.strip() in case there is are spaces around the folder path
    ebook_folders = [os.path.expanduser(f.strip()) for f in config_ini['organize-ebooks']['ebook_folders'].split(',')]
    ipdb.set_trace()
    for fpath in ebook_folders:
        print('Recursively scanning {} for files'.format(fpath))
        # TODO: They make use of sorting flags for walking through the files [FILE_SORT_FLAGS]
        # ref.: https://github.com/na--/ebook-tools/blob/0586661ee6f483df2c084d329230c6e75b645c0b/organize-ebooks.sh#L313
        for path, dirs, files in os.walk(fpath):
            for file in files:
                # TODO: add debug_prefixer
                organize_file(file_path=os.path.join(path, file),
                              corruption_check_only=config_ini['organize-ebooks']['corruption_check_only'],
                              organize_without_isbn=config_ini['organize-ebooks']['organize_without_isbn'])