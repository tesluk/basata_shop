from PIL import Image
from Basatashop.Entities.models import News, Product_group, Product_type,\
    Instruction, Product

def resize_picture(obj):
    path = obj.picture.path
    p = obj.picture.__unicode__().split('.')
    print p 
    path = path.replace('\\entities\\entities', '\\entities')
    
    img = Image.open(path)
    name=path
    #print width, height
    img.thumbnail((500, 500), Image.ANTIALIAS) 
    img.save(name.split('.')[0]+"_b.jpg","JPEG") 
    
    obj.picture_b = p[0]+'_b.jpg'
        
    img.thumbnail((150, 150), Image.ANTIALIAS) 
    img.save(name.split('.')[0]+"_l.jpg","JPEG")  
    
    obj.picture_l = p[0]+'_l.jpg'
    obj.save()
    
def resize_all ():
    
    ns = News.objects.all()
    for n in ns:
        resize_picture(n)
        
    pgs = Product_group.objects.all()
    for pg in pgs:
        resize_picture(pg)
        
    pts = Product_type.objects.all()
    for pt in pts:
        resize_picture(pt)
        
    ins = Instruction.objects.all()
    for i in ins:
        resize_picture(i)
        
    pds = Product.objects.all()
    for pd in pds:
        resize_picture(pd)
        
#resize_all()
    
#n = News.objects.all()[0]
#resize_picture(n)
#n.save()
#path = n.picture.path 
#print path.replace('\\entities\\entities', '\\entities')