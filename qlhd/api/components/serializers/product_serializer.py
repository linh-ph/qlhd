from qlhd.api.utils.util_image import convert_string_to_float
from qlhd.models import Invoice, DetailInvoice


def set_to_database_product(data_table, id_invoice):
    try:
        print("id_distributor", id_invoice)
        invoice = Invoice.objects.get(pk=id_invoice)
        if data_table is not None:
            count = 0
            for i, row in enumerate(data_table):
                count = i + 1
                name = row.get('name')
                unit = row.get('unit')
                quantity = row.get('quantity')
                price = row.get('price')
                total_price = row.get('total_price')
                tax = row.get('tax')
                tax_money = row.get('tax_money')
                total = row.get('total')

                detail = DetailInvoice(name=name, unit=unit, quantity=quantity, price=convert_string_to_float(price),
                                       total_price=convert_string_to_float(total_price),
                                       tax=convert_string_to_float(tax),
                                       tax_money=convert_string_to_float(tax_money), total=convert_string_to_float(total))
                detail.invoice = invoice
                detail.save()

                # p = Product(name=name,
                #             unit=unit, quantity=quantity, price=price, total_price=total_price, tax=tax,
                #             money_tax=money_tax, total=total)
                # p.save()
            return count
        else:
            return 0
    except NameError:
        return 0
