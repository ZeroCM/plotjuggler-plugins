#! /usr/bin/env python
# encoding: utf-8

import waflib
from waflib.Errors import WafError
import os.path

# these variables are mandatory ('/' are converted automatically)
top = '.'
out = 'build'

def options(ctx):
    ctx.load('compiler_c')
    ctx.load('compiler_cxx')

def configure(ctx):
    ctx.setenv('')
    ctx.load('compiler_c')
    ctx.load('compiler_cxx')
    setup_environment(ctx)

def use_elf(ctx):
    if not os.path.exists('/usr/include/libelf.h'):
        raise WafError('Failed to find libelf')
    ctx.env.LIB_elf = ['elf', 'dl']
    return True

def use_plotjuggler(ctx):
    if not os.path.exists('/usr/local/include/PlotJuggler'):
        raise WafError('Failed to find PlotJuggler')
    ctx.env.INCLUDES_plotjuggler = ['/usr/local/include/PlotJuggler']
    ctx.env.LIB_plotjuggler = ['plotjuggler_base']
    return True

def use_zcm(ctx):
    ctx.check_cfg(package='zcm', args='--cflags --libs', uselib_store='zcm')

def use_qt5(ctx):
    ctx.check_cfg(package='Qt5Core', args='--cflags --libs', uselib_store='Qt5Core')
    ctx.check_cfg(package='Qt5Widgets', args='--cflags --libs', uselib_store='Qt5Widgets')
    ctx.check_cfg(package='Qt5Concurrent', args='--cflags --libs', uselib_store='Qt5Concurrent')
    ctx.check_cfg(package='Qt5Xml', args='--cflags --libs', uselib_store='Qt5Xml')
    ctx.check_cfg(package='Qt5Svg', args='--cflags --libs', uselib_store='Qt5Svg')
    ctx.check_cfg(package='Qt5OpenGL', args='--cflags --libs', uselib_store='Qt5OpenGL')
    return True

def setup_environment_gnu(ctx):
    FLAGS = ['-Wno-unused-local-typedefs',
            ]
    ctx.env.CFLAGS_default   += FLAGS
    ctx.env.CXXFLAGS_default += FLAGS

def setup_environment(ctx):
    ctx.post_mode = waflib.Build.POST_LAZY
    ctx.env.SRCPATH = ctx.path.get_src().abspath()

    WARNING_FLAGS = ['-Wall', '-Werror', '-Wno-unused-function']
    SYM_FLAGS = ['-g']
    OPT_FLAGS = ['-O3']
    ctx.env.CFLAGS_default    = ['-std=gnu99', '-fPIC', '-pthread'] + WARNING_FLAGS
    ctx.env.CXXFLAGS_default  = ['-std=c++17', '-fPIC', '-pthread'] + WARNING_FLAGS
    ctx.env.INCLUDES_default  = [ctx.path.abspath()]
    ctx.env.LINKFLAGS_default = ['-pthread']

    use_elf(ctx)
    use_qt5(ctx)
    use_plotjuggler(ctx)
    use_zcm(ctx)

    setup_environment_gnu(ctx)

def build(ctx):
    ctx(target = 'qt5',
        use = ['Qt5Core', 'Qt5Widgets', 'Qt5Concurrent',
               'Qt5Xml', 'Qt5Svg', 'Qt5OpenGL'])

    ctx.recurse('DataStreamZcm')
