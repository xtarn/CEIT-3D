'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p
from OpenGL.GL import glget
EXTENSION_NAME = 'GL_SGIX_texture_add_env'
_p.unpack_constants( """GL_TEXTURE_ENV_BIAS_SGIX 0x80BE""", globals())


def glInitTextureAddEnvSGIX():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )
