# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class Picking(models.Model):
    """ Inherit stock package to constraint one product by package """
    _inherit = "stock.picking"

    def _get_lines_by_product(self):
        self.ensure_one()
        lines_by_product_dict = {}
        lines_by_product = []
        for line in self.move_lines.filtered(lambda mv: mv.state != 'cancel' and mv.product_uom_qty):
            if lines_by_product_dict.get(line.product_id):
                # lots
                if line.move_line_ids and line.state == 'done' and line.move_line_ids.mapped('lot_id'):
                    lines_by_product_dict[line.product_id]['serial_numbers'] |= line.move_line_ids.mapped('lot_id')
                # packages
                packages = []
                if line.move_line_ids and line.state == 'done':
                    packaging_nbr = sum(line.move_line_ids.mapped("packaging_nbr"))
                    incomplete_qty = sum(line.move_line_ids.mapped("incomplete_qty"))
                    for package_move_line in line.move_line_ids:
                        lines_by_product_dict[line.product_id]['packages'].append(
                            {'package': package_move_line.result_package_id or self.env['stock.quant.package'],
                             'qty_by_packaging': package_move_line.qty_by_packaging})
                else:
                    packaging_nbr = line.packaging_nbr
                    incomplete_qty = line.incomplete_qty
                lines_by_product_dict[line.product_id]['product_uom_qty'] += line.product_uom_qty
                lines_by_product_dict[line.product_id]['quantity_done'] += line.quantity_done
                lines_by_product_dict[line.product_id]['packaging_nbr'] += packaging_nbr
                lines_by_product_dict[line.product_id]['incomplete_qty'] += incomplete_qty
            else:
                # lots
                if line.move_line_ids and line.state == 'done' and line.move_line_ids.mapped('lot_id'):
                    serial_numbers = line.move_line_ids.mapped('lot_id')
                else:
                    serial_numbers = self.env['stock.production.lot']
                # packages
                packages = []
                if line.move_line_ids and line.state == 'done':
                    packaging_nbr = sum(line.move_line_ids.mapped("packaging_nbr"))
                    incomplete_qty = sum(line.move_line_ids.mapped("incomplete_qty"))
                    for package_move_line in line.move_line_ids:
                        packages.append({'package': package_move_line.result_package_id or self.env['stock.quant.package'],
                                         'qty_by_packaging': package_move_line.qty_by_packaging})

                else:
                    packaging_nbr = line.packaging_nbr
                    incomplete_qty = line.incomplete_qty
                lines_by_product_dict.update({line.product_id: {'serial_numbers': serial_numbers,
                                                                'picking_id': line.picking_id,
                                                                'product_uom_qty': line.product_uom_qty,
                                                                'quantity_done': line.quantity_done,
                                                                'product_uom': line.product_uom,
                                                                'prepress_proof_id': line.sale_line_id and line.sale_line_id.prepress_proof_id or False,
                                                                'client_ref': line.sale_line_id and line.sale_line_id.prepress_proof_id and
                                                                              line.sale_line_id.prepress_proof_id.client_ref or False,
                                                                'packages': packages,
                                                                'packaging_nbr': packaging_nbr,
                                                                'incomplete_qty': incomplete_qty,
                                                                }})
        for product, line in lines_by_product_dict.items():
            line.update({'product_id': product})
            lines_by_product.append(line)
        return lines_by_product
