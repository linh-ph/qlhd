from api.models import Product, Distributor


def set_to_database_product(text_info_table, id_insert, context):
    try:
        d = Distributor.objects.get(pk=id_insert)
        count = 0
        product_id = []
        for i, row in enumerate(text_info_table):
            count = i + 1

            name = row.get('name')
            unit = row.get('unit')
            quantity = row.get('quantity')
            price = row.get('price')
            total_price = row.get('total_price')
            tax = row.get('tax')
            money_tax = row.get('money_tax')
            total = row.get('total')

            p = Product(name=name,
                        unit=unit, quantity=quantity, price=price, total_price=total_price, tax=tax,
                        money_tax=money_tax, total=total)

            p.id_distributor = d
            p.save()
            product_id.append(p.id)
        return {'error': False, 'count': count, 'product_id': product_id}
    except:
        context['message'] = "Có lỗi xảy ra khi thêm vào product"
        return context
