'''
import platform

__all__ = ["backup", "back_to_yesterday", "get", "mail"]
if platform.system() == 'Windows':
    __all__.append("spvoice")
'''