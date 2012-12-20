from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
import  settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Basatashop.views.home', name='home'),
    # url(r'^Basatashop/', include('Basatashop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     
     # START TAB
     (r'^questions/$', 'Questions.views.get_quest_list'),
     (r'^questions/delete/(\d{1,3})/$', 'Questions.views.delete_question'),
     (r'^questions/ans/(\d{1,3})/$', 'Questions.views.get_add_answer'),
     (r'^questions/addans/(\d{1,3})/$', 'Questions.views.add_answer'),
      (r'^questions/addquest/$', 'Questions.views.add_quest'),
      
      (r'^products/delete/(\d{1,3})/$', 'Products.views.delete_prod_group'),
      (r'^products/delete/(\d{1,3})/(\d{1,3})/$', 'Products.views.delete_prod_type'),
      (r'^products/delete/(\d{1,3})/(\d{1,3})/(\d{1,3})/$', 'Products.views.delete_prod'),                   
#      (r'^products/edit/(\d{1,3})/$', 'Products.views.get_edit_prod_group'),
#      (r'^products/edit/(\d{1,3})/(\d{1,3})/$', 'Products.views.get_edit_prod_type'),
#      (r'^products/edit/(\d{1,3})/(\d{1,3})/(\d{1,3})/$', 'Products.views.get_edit_prod'),
      (r'^products/$', 'Products.views.get_all_groups'),
      (r'^products/(\d{1,3})/$', 'Products.views.get_prod_group'),
      (r'^products/(\d{1,3})/(\d{1,3})/$', 'Products.views.get_prod_type'),
      (r'^products/(\d{1,3})/(\d{1,3})/(\d{1,3})/$', 'Products.views.get_prod'),    
      (r'^products/addgroup/$', 'Products.views.get_add_group'),
      (r'^products/addtype/(\d{1,3})/$', 'Products.views.get_add_type'),
      (r'^products/addproduct/(\d{1,3})/$', 'Products.views.get_add_prod'),  
      (r'^products/addchar/(\d{1,3})/$', 'Products.views.get_add_char'),  
      
      
      (r'^products/newgroup/$', 'Products.views.add_group'),
      (r'^products/newtype/(\d{1,3})/$', 'Products.views.add_type'),

      (r'^products/newproduct/(\d{1,3})/$', 'Products.views.add_prod'),
      (r'^products/newchar/(\d{1,3})/$', 'Products.views.add_char'),      
#      (r'^products/savegroup/(\d{1,3})/$', 'Products.views.save_group'),
#      (r'^products/savetype/(\d{1,3})/$', 'Products.views.save_type'),
#      (r'^products/saveproduct/(\d{1,3})/$', 'Products.views.save_prod'),

    (r'^products/(\d{1,3})/(\d{1,3})/(\d{1,3})/graphics/$', 'Products.views.show_graphics'),    

     (r'^basket/$', 'Basket.views.get_basket'),
     (r'^basket/add/(\d{1,3})/$', 'Basket.views.add_product'),
     (r'^basket/delete/(\d{1,3})/$', 'Basket.views.delete_char'),
     (r'^basket/update/$', 'Basket.views.update_basket'),
     (r'^basket/order/$', 'Basket.views.get_order'),
     (r'^basket/addorder/$', 'Basket.views.get_ready'),
     
     (r'^accounts/profile/$', 'basatashop.views.index'),
     # END TAB

     
     #START BODIA
    url(r'^$', 'basatashop.views.index'),
    url(r'^about/$', 'basatashop.views.about'),
    url(r'^contacts/$', 'basatashop.views.contacts'),
    url(r'^delivery/$', 'basatashop.views.delivery'),
    
    url(r'^basket/order_state/$', 'Basket.views.order_state'),
    url(r'^basket/finish_order/$', 'Basket.views.finish_order'),
    #END BODIA 
    
    #START SEKAS
    url(r'^accounts/register/$', 'registration.views.sregister'),
    url(r'accounts/login/$', 'registration.views.login'),
    url(r'accounts/logout/$', 'registration.views.logout'),
    url(r'^register/edit/$', 'registration.views.sregister_edit'),
    
    #(r'^accounts/', include('registration.backends.default.urls')),
    #url(r'^register/edit/$', register_edit, name='registration_edit'),
    #END SEKAS
     
     #START TANIA
     ('^news/$', 'news.views.show_news'),
     ('^news/add_news/$', 'news.views.add_news'),
     ('^submit_news/$', 'news.views.submit_news'),
     ('^wholesale/$', 'wholesalers.views.wholesale'),
     ('^add_company/$', 'wholesalers.views.add_company'),
     ('^submit_company/$', 'wholesalers.views.submit_company'),
     (r'^wholesale/(\d{1,3})/$', 'wholesalers.views.file_download'),
     (r'^delete/(\d{1,3})/$', 'wholesalers.views.file_delete'),
     ('^add_doc/$', 'wholesalers.views.add_doc'),
     ('^submit_doc/$', 'wholesalers.views.submit_doc'),
     
     ('^edit_company/$', 'wholesalers.views.edit_company'),
     ('^esubmit_company/$', 'wholesalers.views.esubmit_company'),
     #END TANIA
     
     #START NASTIA
     (r'^instructions/$', 'instructions.views.all_instructions'),
     (r'^instructions/add_new/$', 'instructions.views.get_add_instruct'),
     (r'^instructions/newinstruct/$', 'instructions.views.add_instruct'),
     (r'^instructions/edit/(\d{1,3})/$', 'instructions.views.edit'),
     (r'^instructions/delete/(\d{1,3})/$', 'instructions.views.delete'),
     (r'^instructions/saveedited/(\d{1,3})/$', 'instructions.views.save_edited'),
     
#     (r'^products/edit/(\d{1,3})/$', 'Products.views.edit'),
#     (r'^products/delete/(\d{1,3})/$', 'Products.views.delete'),
#     (r'^products/saveedited/(\d{1,3})/$', 'Products.views.save_edited'),
     #END NASTIA
     
     # XML
     (r'^xml/groups/$', 'Products.views.get_all_groups_xml'),
     (r'^xml/types/(\d{1,3})$', 'Products.views.get_types_xml'),
     (r'^xml/products/(\d{1,3})$', 'Products.views.get_products_xml'),
     # end XML
)
