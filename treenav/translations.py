from modeltranslation.translator import translator, TranslationOptions
from treenav.models import MenuItem


class MenuItemOptions(TranslationOptions):
    fields = ('label', )
translator.register(MenuItem, MenuItemOptions)
