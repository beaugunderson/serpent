import os
import platform
import sys

from distutils import cygwinccompiler
from distutils.sysconfig import get_config_vars

from setuptools import setup, Extension


def patch_get_msvcr():
    # From http://stackoverflow.com/a/34427014
    _get_msvcr = cygwinccompiler.get_msvcr

    def get_msvcr():
        try:
            return _get_msvcr()
        except ValueError:
            msc_pos = sys.version.find('MSC v.')

            if msc_pos != -1:
                msc_ver = sys.version[msc_pos+6:msc_pos+10]

                if msc_ver == '1700':
                    # Visual Studio 2012 / Visual C++ 11.0
                    return ['msvcr110']
                elif msc_ver == '1800':
                    # Visual Studio 2013 / Visual C++ 12.0
                    return ['msvcr120']
                elif msc_ver == '1900':
                    # Visual Studio 2015 / Visual C++ 14.0
                    # "msvcr140.dll no longer exists"
                    # http://blogs.msdn.com/b/vcblog/archive/2014/06/03/visual-studio-14-ctp.aspx
                    return ['vcruntime140']
                else:
                    raise

    return get_msvcr


cygwinccompiler.get_msvcr = patch_get_msvcr()

(opt,) = get_config_vars('OPT')
if opt is not None:
    os.environ['OPT'] = ' '.join(
        flag for flag in opt.split() if flag != '-Wstrict-prototypes'
    )

include_dirs = []
library_dirs = []
extra_compile_args = []

if platform.system() == 'Windows':
    if os.getenv('COMPILER') == 'mingw':
        extra_compile_args.append('-D_hypot=hypot')
        extra_compile_args.append('-Wno-sign-compare')

    if os.getenv('PYTHON_ARCH') == '64':
        extra_compile_args.append('-DMS_WIN64')

    if os.getenv('PYTHON_VERSION') == '3.6.x':
        library_dirs.append(os.getenv('PYTHON'))
else:
    extra_compile_args.append('-Wno-sign-compare')

setup(
    # Name of this package
    name='ethereum-serpent-augur-temp',

    # Package version
    version='2.0.2',

    description='Serpent compiler',
    maintainer='Vitalik Buterin',
    maintainer_email='v@buterin.com',
    license='WTFPL',
    url='http://www.ethereum.org/',

    # Describes how to build the actual extension module from C source files.
    ext_modules=[
        Extension(
            'serpent_pyext',         # Python name of the module
            sources=['keccak-tiny.cpp', 'bignum.cpp', 'util.cpp',
                     'tokenize.cpp', 'lllparser.cpp', 'parser.cpp',
                     'functions.cpp', 'optimize.cpp', 'opcodes.cpp',
                     'rewriteutils.cpp', 'preprocess.cpp', 'rewriter.cpp',
                     'compiler.cpp', 'funcs.cpp', 'pyserpent.cpp'],
            include_dirs=include_dirs,
            library_dirs=library_dirs,
            extra_compile_args=extra_compile_args)
    ],
    py_modules=[
        'serpent',
        'pyserpent'
    ],
    scripts=[
        'serpent.py'
    ],
    entry_points={
        'console_scripts': [
            'serpent = serpent:main',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
