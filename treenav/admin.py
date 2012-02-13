#import new

from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes import generic
from django import forms

from mptt.admin import MPTTModelAdmin

from treenav import models as treenav
from treenav.forms import MenuItemForm, GenericInlineMenuItemForm

INLINE_PREPOPULATED = {'slug': ('label',)}

MenuItemAdmin = admin.ModelAdmin
GenericStackedInline = generic.GenericStackedInline
SubMenuItemInlineAdmin = admin.StackedInline
# SubMenuItemInlineAdmin = admin.TabularInline # defaults, but doesn't play well with grappelli

#if 'grappellifit' in settings.INSTALLED_APPS and 'modeltranslation' in settings.INSTALLED_APPS:
#    from grappellifit.admin import TranslationAdmin, TranslationGenericStackedInline, TranslationStackedInline, translator
#    INLINE_PREPOPULATED = {}  # broken for inlines :(
#    if translator.is_registred('MenuItem'):
#        MenuItemAdmin = TranslationAdmin
#        SubMenuItemInlineAdmin = TranslationStackedInline
if 'grappellifit' in settings.INSTALLED_APPS and 'modeltranslation' in settings.INSTALLED_APPS:
    from grappellifit.admin import TranslationAdmin, TranslationGenericStackedInline, TranslationStackedInline, translator
    INLINE_PREPOPULATED = {}  # broken for inlines :(
    if translator.is_registred('MenuItem'):
        #MenuItemAdmin = TranslationAdmin
        #SubMenuItemInlineAdmin = TranslationStackedInline
        class ToSubClass(MPTTModelAdmin, TranslationAdmin): pass
    else:
        class ToSubClass(MPTTModelAdmin): pass
else:
    class ToSubClass(MPTTModelAdmin): pass

if 'grappellifit' in settings.INSTALLED_APPS:
    CHANGE_LIST_TEMPLATE = 'admin/treenav/menuitem/mptt_change_list.html'
else:
    CHANGE_LIST_TEMPLATE = 'admin/mptt_change_list.html'


class GenericMenuItemInline(GenericStackedInline):
    """
    Add this inline to your admin class to support editing related menu items
    from that model's admin page.
    """
    extra = 0
    max_num = 1
    model = treenav.MenuItem
    form = GenericInlineMenuItemForm


class SubMenuItemInline(SubMenuItemInlineAdmin):
    model = treenav.MenuItem
    extra = 1
    form = MenuItemForm
    prepopulated_fields = INLINE_PREPOPULATED


class MenuItemAdmin(ToSubClass):
    list_display = (
        'slug',
        'label',
        'parent',
        'link',
        'href_link',
        'order',
        'lft', 
        'rght',
        'is_enabled',
    )
    change_list_template = CHANGE_LIST_TEMPLATE    
    list_filter = ('parent', 'is_enabled')
    prepopulated_fields = {'slug': ('label_en',)}
    inlines = (SubMenuItemInline,)
    fieldsets = (
        (None, {
            'fields': ('parent', 'label', 'slug', 'order', 'is_enabled')
        }),
        ('URL', {
            'fields': ('link', ('content_type', 'object_id')),
            'description': "The URL for this menu item, which can be a "
                           "fully qualified URL, an absolute URL, a named "
                           "URL, a path to a Django view, a regular "
                           "expression, or a generic relation to a model that "
                           "supports get_absolute_url()"
        }),
    )
    list_editable = ('label', 'order',)
    form = MenuItemForm
    
    def href_link(self, obj):
        return '<a href="%s">%s</a>' % (obj.href, obj.href)
    href_link.short_description = 'HREF'
    href_link.allow_tags = True

admin.site.register(treenav.MenuItem, MenuItemAdmin)
