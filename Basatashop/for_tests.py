from Basatashop.Entities.models import News, Product_group

a = [1, 2, 5, 'a', 'd']

print a

for e in a:
    if e == 5 or e == 'a':
        a.remove(e)
print a