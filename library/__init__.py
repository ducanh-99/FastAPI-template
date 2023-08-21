try:
    __import__('pkg_resources').declare_namespace('tekone')
except ImportError:
    __path__ = __import__('pkgutil').extend_path(__path__, 'tekone')