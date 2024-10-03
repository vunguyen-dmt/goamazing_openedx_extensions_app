"""
goamazing_openedx_extensions_app Django application initialization.
"""

from django.apps import AppConfig


class GoamazingOpenedxExtensionsAppConfig(AppConfig):
    """
    Configuration for the goamazing_openedx_extensions_app Django application.
    """

    name = 'goamazing_openedx_extensions_app'

    plugin_app = {
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'goamazing_openedx_extensions_app',
                'regex': '^api/goamazing_openedx_extensions_app/',
            }
        },
    }
