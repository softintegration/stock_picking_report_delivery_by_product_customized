# -*- coding: utf-8 -*- 


{
    'name': 'Picking delivery slip by product customized',
    'author': 'Soft-integration',
    'application': False,
    'installable': True,
    'auto_install': False,
    'qweb': [],
    'description': False,
    'images': [],
    'version': '1.0.1.1',
    'category': 'Inventory/Inventory',
    'demo': [],
    'depends': ['stock_picking_report_delivery_by_product',
                'stock_picking_report_title',
                'sale_stock_prepress_management',
                'sale_stock',
                'stock_picking_transportation_info',
                'stock_picking_report_signature',
                'stock_picking_report_customer_signature',
                'stock_picking_packaging_control'],
    'data': [
        'data/stock_picking_report_delivery_by_product_data.xml',
        'report/report_deliveryslip_by_product.xml'
    ],
    'license': 'LGPL-3',
}
