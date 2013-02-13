'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p, constants as _cs, arrays
from OpenGL.GL import glget
import ctypes
EXTENSION_NAME = 'GL_ARB_transform_feedback2'
def _f( function ):
    return _p.createFunction( function,_p.GL,'GL_ARB_transform_feedback2',False)
_p.unpack_constants( """GL_TRANSFORM_FEEDBACK 0x8E22
GL_TRANSFORM_FEEDBACK_PAUSED 0x8E23
GL_TRANSFORM_FEEDBACK_ACTIVE 0x8E24
GL_TRANSFORM_FEEDBACK_BINDING 0x8E25""", globals())
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint)
def glBindTransformFeedback( target,id ):pass
@_f
@_p.types(None,_cs.GLsizei,arrays.GLuintArray)
def glDeleteTransformFeedbacks( n,ids ):pass
@_f
@_p.types(None,_cs.GLsizei,arrays.GLuintArray)
def glGenTransformFeedbacks( n,ids ):pass
@_f
@_p.types(_cs.GLboolean,_cs.GLuint)
def glIsTransformFeedback( id ):pass
@_f
@_p.types(None,)
def glPauseTransformFeedback(  ):pass
@_f
@_p.types(None,)
def glResumeTransformFeedback(  ):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint)
def glDrawTransformFeedback( mode,id ):pass


def glInitTransformFeedback2ARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )
