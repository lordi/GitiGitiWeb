from django.conf.urls.defaults import *

urlpatterns = patterns('giti.views',
    # Meta-repository operations
    (r'^$', 'repository_list'),

    # Operations on blobs
    (r'^show/(?P<repo_name>[^/]+)/(?P<path>.*)$', 'show'),
    (r'^raw/(?P<repo_name>[^/]+)/(?P<path>.*)$', 'raw'),
    (r'^edit/(?P<repo_name>[^/]+)/(?P<path>.*)$', 'edit'),
    (r'^delete/(?P<repo_name>[^/]+)/(?P<path>.*)$', 'delete'),
    (r'^stage/(?P<repo_name>[^/]+)/(?P<path>.*)$', 'stage'),
    
    # Operations on trees
    (r'^list/(?P<repo_name>[^/]+)/(?P<path>.*)$', 'tree_show'),
    
    # Operations on the index
    (r'^commit/(?P<repo_name>[^/]+)/$', 'index_commit'),
    (r'^revert/(?P<repo_name>[^/]+)/$', 'index_revert'),
    (r'^remove/(?P<repo_name>[^/]+)/(?P<path>.*)$', 'index_remove'),
)
