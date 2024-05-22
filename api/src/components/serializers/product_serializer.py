from qlhd.models import Distributor, Product


def set_to_database_product(text_info_table, id_insert):
    try:
        d = Distributor.objects.get(pk=id_insert)
        if (text_info_table is not None):
            count = 0
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

          
            return count
        else:
          
            return 0

    except NameError:
        return 0
