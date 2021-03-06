'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p, constants as _cs, arrays
from OpenGL.GL import glget
import ctypes
EXTENSION_NAME = 'GL_EXT_index_func'
def _f( function ):
    return _p.createFunction( function,_p.GL,'GL_EXT_index_func',False)
_p.unpack_constants( """GL_INDEX_TEST_EXT 0x81B5
GL_INDEX_TEST_FUNC_EXT 0x81B6
GL_INDEX_TEST_REF_EXT 0x81B7""", globals())
@_f
@_p.types(None,_cs.GLenum,_cs.GLclampf)
def glIndexFuncEXT( func,ref ):pass


def glInitIndexFuncEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )
