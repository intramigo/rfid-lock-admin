from django.views.generic import list_detail
from django.views.generic.simple import redirect_to, direct_to_template
from django.conf.urls import patterns, include, url
from djock_app.models import RFIDkeycard, Door
from djock_app import views
from django.http import HttpResponse
from django.shortcuts import redirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# This is a view, but putting it in here to "test" stuff
#def blah(request, doorid, rfid):
def blah(request):

    return list_detail.object_list(
        request,
        queryset = RFIDkeycard.objects.all(), 
       # template_name = "basic.html",
        #template_object_name = "rfidkeycard_list",  # So in template,  {% for rfidkeycard in rfidkeycard_list %} instead of   {% for rfidkeycard in object_list %} .....  although something isn't working.....
        #extra_context = {"params" :{'doorid': doorid, 'rfid':rfid}, \
        #                "doors_list": Door.objects.all(), 
        #                 }
    )


urlpatterns = patterns('',
    url(r'test_jquery/$',views.test_jquery),
    url(r'start_scan/(?P<lockuser_object_id>\d+)/$',views.initiate_new_keycard_scan), 
    url(r'done_scan/(?P<lockuser_object_id>\d+)/$',views.finished_new_keycard_scan), 

    # door id is an int with no specified length (for now?);
    # rfid is expected to be a string exactly 10 characters long
    url(r'checkdoor/(?P<doorid>\d+)/checkrfid/(?P<rfid>\w{10})/$',\
                        views.check, \
                        #list_detail.object_list, \
                        #rfidkeycard_info
                        #direct_to_template, {'template': 'basic.html' }, \

    ),





 #   url(r'door/(?P<doorid>\d+)/checkrfid/(?P<rfid>\w{10})/$',\
 #                       blah, \
                        #list_detail.object_list, \
                        #rfidkeycard_info
                        #direct_to_template, {'template': 'basic.html' }, \

  #  ),






    # Uncomment the next line to enable the admin:
    url(r'^lockadmin/', include(admin.site.urls)),

    # go directly to the admin page for the *application*
    url(r'^lock/$',redirect_to, {'url': '/lockadmin/djock_app/'}),

    # is this rfid allowed to access this door
    # (keeping door identifier just numerical for now)
    # (direct_to_template right now, just a quick demo of displaying arguments in the url,
    #   in an HTML template... Not actually performing the check yet... So will need a view. 
    # [ But since all I have to send back is a 1 or 0, maybe I don't have to write a template at all?])
    # direct_to_template passes the dictionary 'params' to the template, so to
    #   access 'doorid,' for example, you have to do {{ params.doorid }} )
    url(r'/door/(?P<doorid>\d+)/checkrfid/(?P<rfid>\d+)/$',\
                        direct_to_template, {'template': 'basic.html' }, \

    ),

    # get list of rfid's allowed to open this door
    # direct_to_template right now, just a quick demo of displaying arguments in the url,
    # not displaying the objects yet
    # (later, in view, something like -
    #   return HttpResponse(data, mimetype='application/json')
    #url(r'^door/(?P<doorid>\d+)/getallowed/$', direct_to_template, {'template': 'we_are_ok.html' }    ),
    #url(r'checkdoor/(?P<doorid>\d+)/getallowed/$', direct_to_template, {'template': 'admin/we_are_ok.html' }    ),
    url(r'door/(?P<doorid>\d+)/getallowed/$', views.get_allowed_rfids ), 
    url(r'^checkdoor/(?P<doorid>\d+)/getallowed/$', direct_to_template, {'template': 'admin/we_are_ok.html' }    ),

    url(r'deactivate_keycard/(?P<object_id>\d+)/$', views.deactivate_keycard),

    # testing stuff/temp
    url(r'^t/$', direct_to_template, {'template': 'test/index.html' }    ),
    #url(r'fake/$', 'djock_app.views.fake_assign' ), 

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)

