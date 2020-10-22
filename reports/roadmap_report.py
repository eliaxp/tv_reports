# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.tools.float_utils import float_round as round
from openerp.exceptions import ValidationError, Warning
from datetime import timedelta, date, datetime, time
from num2words import num2words

import locale
import logging

_logger = logging.getLogger(__name__)

class RoadMapReport(models.AbstractModel):

	_name = 'report.tv_reports.roadmap_report'

	@api.multi
	@api.model
	def get_report_values(self, docids, data=None):
		list_so = list()
		dict_roadmap = dict()

		try:
			locale.setlocale(locale.LC_TIME, 'es_AR.UTF-8')
		except Exception as e:
			raise ValidationError(e)
		
		report_obj = self.env['ir.actions.report']
		report = report_obj._get_report_from_name('tv_reports.roadmap_report')

		find_sale_order = self.env['sale.order'].search([
			('id', 'in', docids)
		])

		for so in find_sale_order:
			dict_so = { 'categories': [] }
			total_burganas = 0
			total_caja_burganas = 0
			total_frutas_gr = 0
			total_frutas_ch = 0
			total_rebozados_kari = 0
			total_bites = 0
			total_torta = 0
			total_haulani_180 = 0
			total_haulani_500 = 0
			total_kaira_cla_250 = 0
			total_kaira_liv_500 = 0
			total_kaira_liv_250 = 0
			total_kaira_liv_120 = 0
			total_ravioles = 0
			total_postre = 0
			total_samosas_ch = 0
			total_pizza = 0
			total_pizza_veg = 0
			total_croqueta = 0
			total_station = 0
			total_kari_yogt_ch = 0
			total_kari_yogt_gr = 0
			total_amoedo_tarta = 0
			total_amoedo_integral = 0
			total_casa_vegana = 0
			total_casa_vegana_toq = 0
			total_vivet_leche = 0
			total_vivet_queso = 0
			total_sirius = 0
			total_placer = 0
			total_quimya = 0
			total_fv_cheddar = 0
			total_fv_provoleta = 0
			total_fv_mozza = 0 
			total_fv_hummus = 0
			total_fv_yogurt = 0
			total_fv_dulce_ch = 0
			total_fv_dulce_gr = 0
			total_fv_alfajor = 0
			total_logo = 0
			total_cudda_hormita = 0
			total_cudda_untable = 0
			total_nina_refr = 0
			total_quimya_yog = 0
			total_augus_untable = 0
			total_augus_horma = 0
			total_kombucha_refr = 0
			total_fv_botell_ch = 0
			total_fv_crema  = 0
			total_jugo_litro = 0
			total_cacah_vivet = 0
			total_notco = 0
			total_silk_refr = 0
			total_dale_coco_refr = 0
			total_sonder = 0
			total_vivet_cacahuate = 0
			total_quimya_granola = 0
			total_kombucha = 0
			total_felices_alfajor = 0
			total_nina_sec = 0
			total_pf_litro = 0
			total_pf_500ml = 0
			total_pf_330ml = 0
			total_pf_200ml = 0
			total_notmayo = 0
			total_notmilk = 0
			total_silk = 0
			total_dale_coco = 0

			# Diccionarios para categoría ecommerce congelados
			burganas, \
			caja_burganas, \
			frutas_gr, \
			frutas_ch, \
			rebozados_kari, \
			bites, \
			tortas, \
			haulani_180, \
			haulani_500, \
			kaira_cla_250, \
			kaira_liv_500, \
			kaira_liv_250, \
			kaira_liv_120, \
			ravioles, \
			postre, \
			samosas_ch, \
			pizza, \
			pizza_veg, \
			croqueta,  \
			station, \
			kari_yogt_ch, \
			kari_yogt_gr, \
			amoedo_tarta, \
			amoedo_integral = self._init_dict_items_congelados()
			# Diccionarios para categoría ecommerce refrigerados
			casa_vegana, \
			casa_vegana_toq, \
			vivet_leche, \
			vivet_queso, \
			sirius, \
			placer, \
			quimya, \
			fv_cheddar, \
			fv_provoleta, \
			fv_mozza, \
			fv_hummus, \
			fv_yogurt, \
			fv_dulce_ch, \
			fv_dulce_gr, \
			fv_alfajor, \
			logo, \
			cudda_hormita, \
			cudda_untable, \
			nina_refr, \
			quimya_yog, \
			augus_untable, \
			augus_horma, \
			kombucha_refr, \
			fv_botell_ch, \
			fv_crema, \
			jugo_litro, \
			cacah_vivet, \
			notco, \
			silk_refr, \
			dale_coco_refr, \
			sonder = self._init_dict_items_refrigerados()
			# Diccionarios para categoría ecommerce secos
			vivet_cacahuate, quimya_granola, kombucha, felices_alfajor, nina_sec, pf_litro, pf_500ml, pf_330ml, pf_200ml, notmayo, notmilk, silk, dale_coco = self._init_dict_items_secos()
			date_order = datetime.strptime(so.date_order, "%Y-%m-%d %H:%M:%S").strftime('%A %d')
			name = so.name

			report_has_congelados = False
			report_has_refrigerados = False
			report_has_secos = False
			for line in so.order_line:
				categ_ecomm_name = None
				for rec in line.product_id.public_categ_ids:
					if rec.name.lower() in ['congelados', 'refrigerados', 'secos']:
						categ_ecomm_name = rec.name

				if categ_ecomm_name != None:
					categ_ecomm = categ_ecomm_name.lower()
					if categ_ecomm == 'congelados':
						if line.product_id.categ_id:
							categ_int = None
							product_ref_int = line.product_id.default_code
							if ' ' in line.product_id.categ_id.name:
								str_replace = line.product_id.categ_id.name.lower().split(' ')
								categ_int = "%s_%s" %(str_replace[0], str_replace[1])
							else:
								categ_int = line.product_id.categ_id.name.lower()

							if categ_int == 'burganas':
								if product_ref_int == 'berenjena_burganas':
									burganas['berenjena'] = (burganas['berenjena'] + line.product_uom_qty)
									total_burganas = (total_burganas + line.product_uom_qty)
								elif product_ref_int == 'brocoli_burganas':
									burganas['brocoli'] = (burganas['brocoli'] + line.product_uom_qty)
									total_burganas = (total_burganas + line.product_uom_qty)
								elif product_ref_int == 'calabaza_burganas':
									burganas['calabaza'] = (burganas['calabaza'] + line.product_uom_qty)
									total_burganas = (total_burganas + line.product_uom_qty)
								elif product_ref_int == 'cebolla_burganas':
									burganas['cebolla'] = (burganas['cebolla'] + line.product_uom_qty)
									total_burganas = (total_burganas + line.product_uom_qty)
								elif product_ref_int == 'espinaca_burganas':
									burganas['espinaca'] = (burganas['espinaca'] + line.product_uom_qty)
									total_burganas = (total_burganas + line.product_uom_qty)
								elif product_ref_int == 'lentejas_burganas':
									burganas['lentejas'] = (burganas['lentejas'] + line.product_uom_qty)
									total_burganas = (total_burganas + line.product_uom_qty)
								elif product_ref_int == 'tomate_burganas':
									burganas['tomate'] = (burganas['tomate'] + line.product_uom_qty)
									total_burganas = (total_burganas + line.product_uom_qty)
								elif product_ref_int == 'romero_burganas':
									burganas['romero'] = (burganas['romero'] + line.product_uom_qty)
									total_burganas = (total_burganas + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))
							
							elif categ_int == 'caja_burganas':
								if product_ref_int == 'caja_berenjena_caja_burganas':
									caja_burganas['caja_berenjena'] = (caja_burganas['caja_berenjena'] + line.product_uom_qty)
									total_caja_burganas = (total_caja_burganas + line.product_uom_qty)
								elif product_ref_int == 'galletitas_caja_burganas':
									caja_burganas['galletitas'] = (caja_burganas['galletitas'] + line.product_uom_qty)
									total_caja_burganas = (total_caja_burganas + line.product_uom_qty)
								elif product_ref_int == 'caja_calabaza_caja_burganas':
									caja_burganas['caja_calabaza'] = (caja_burganas['caja_calabaza'] + line.product_uom_qty)
									total_caja_burganas = (total_caja_burganas + line.product_uom_qty)
								elif product_ref_int == 'caja_cebolla_caja_burganas':
									caja_burganas['caja_cebolla'] = (caja_burganas['caja_cebolla'] + line.product_uom_qty)
									total_caja_burganas = (total_caja_burganas + line.product_uom_qty)
								elif product_ref_int == 'caja_espinaca_caja_burganas':
									caja_burganas['caja_espinaca'] = (caja_burganas['caja_espinaca'] + line.product_uom_qty)
									total_caja_burganas = (total_caja_burganas + line.product_uom_qty)
								elif product_ref_int == 'caja_lentejas_caja_burganas':
									caja_burganas['caja_lentejas'] = (caja_burganas['caja_lentejas'] + line.product_uom_qty)
									total_caja_burganas = (total_caja_burganas + line.product_uom_qty)
								elif product_ref_int == 'caja_tomate_caja_burganas':
									caja_burganas['caja_tomate'] = (caja_burganas['caja_tomate'] + line.product_uom_qty)
									total_caja_burganas = (total_caja_burganas + line.product_uom_qty)
								elif product_ref_int == 'caja_zanahoria_caja_burganas':
									caja_burganas['caja_zanahoria'] = (caja_burganas['caja_zanahoria'] + line.product_uom_qty)
									total_caja_burganas = (total_caja_burganas + line.product_uom_qty)
								elif product_ref_int == 'caja_surtida_caja_burganas':
									caja_burganas['caja_surtida'] = (caja_burganas['caja_surtida'] + line.product_uom_qty)
									total_caja_burganas = (total_caja_burganas + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'haulani_180':
								if product_ref_int == 'coco_haulani_180':
									haulani_180['coco'] = (haulani_180['coco'] + line.product_uom_qty)
									total_haulani_180 = (total_haulani_180 + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'haulani_500':
								if product_ref_int == 'frutilla_haulani_500':
									haulani_500['frutilla'] = (haulani_500['frutilla'] + line.product_uom_qty)
									total_haulani_500 = (total_haulani_500 + line.product_uom_qty)
								elif product_ref_int == 'dulce_de_leche_haulani_500':
									haulani_500['dulce_de_leche'] = (haulani_500['dulce_de_leche'] + line.product_uom_qty)
									total_haulani_500 = (total_haulani_500 + line.product_uom_qty)
								elif product_ref_int == 'chocolate_haulani_500':
									haulani_500['chocolate'] = (haulani_500['chocolate'] + line.product_uom_qty)
									total_haulani_500 = (total_haulani_500 + line.product_uom_qty)
								elif product_ref_int == 'mantequilla_haulani_500':
									haulani_500['mantequilla'] = (haulani_500['mantequilla'] + line.product_uom_qty)
									total_haulani_500 = (total_haulani_500 + line.product_uom_qty)
								elif product_ref_int == 'blanco_haulani_500':
									haulani_500['blanco'] = (haulani_500['blanco'] + line.product_uom_qty)
									total_haulani_500 = (total_haulani_500 + line.product_uom_qty)
								elif product_ref_int == 'matcha_haulani_500':
									haulani_500['matcha'] = (haulani_500['matcha'] + line.product_uom_qty)
									total_haulani_500 = (total_haulani_500 + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'kaira_cla_250':
								if product_ref_int == 'dulce_de_leche_kaira_cla_250':
									kaira_cla_250['dulce_de_leche'] = (kaira_cla_250['dulce_de_leche'] + line.product_uom_qty)
									total_kaira_cla_250 = (total_kaira_cla_250 + line.product_uom_qty)
								elif product_ref_int == 'chocolate_kaira_cla_250':
									kaira_cla_250['chocolate'] = (kaira_cla_250['chocolate'] + line.product_uom_qty)
									total_kaira_cla_250 = (total_kaira_cla_250 + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'kaira_liv_500':
								if product_ref_int == 'chocolate_kaira_liv_500':
									kaira_liv_500['chocolate'] = (kaira_liv_500['chocolate'] + line.product_uom_qty)
									total_kaira_liv_500 = (total_kaira_liv_500 + line.product_uom_qty)
								elif product_ref_int == 'banana_split_kaira_liv_500':
									kaira_liv_500['banana_split'] = (kaira_liv_500['banana_split'] + line.product_uom_qty)
									total_kaira_liv_500 = (total_kaira_liv_500 + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'kaira_liv_250':
								if product_ref_int == 'chocolate_kaira_liv_250':
									kaira_liv_250['chocolate'] = (kaira_liv_250['chocolate'] + line.product_uom_qty)
									total_kaira_liv_250 = (total_kaira_liv_250 + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'kaira_liv_120':
								if product_ref_int == 'chocolate_kaira_liv_120':
									kaira_liv_120['chocolate'] = (kaira_liv_120['chocolate'] + line.product_uom_qty)
									total_kaira_liv_120 = (total_kaira_liv_120 + line.product_uom_qty)
								elif product_ref_int == 'banana_split_kaira_liv_120':
									kaira_liv_120['banana_split'] = (kaira_liv_120['banana_split'] + line.product_uom_qty)
									total_kaira_liv_120 = (total_kaira_liv_120 + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'ravioles':
								if product_ref_int == 'calabaza_ravioles':
									ravioles['calabaza'] = (ravioles['calabaza'] + line.product_uom_qty)
									total_ravioles = (total_ravioles + line.product_uom_qty)
								elif product_ref_int == 'espinaca_ravioles':
									ravioles['espinaca'] = (ravioles['espinaca'] + line.product_uom_qty)
									total_ravioles = (total_ravioles + line.product_uom_qty)
								elif product_ref_int == 'champi_ravioles':
									ravioles['champi'] = (ravioles['champi'] + line.product_uom_qty)
									total_ravioles = (total_ravioles + line.product_uom_qty)
								elif product_ref_int == '4_quesos_ravioles':
									ravioles['4_quesos'] = (ravioles['4_quesos'] + line.product_uom_qty)
									total_ravioles = (total_ravioles + line.product_uom_qty)
								elif product_ref_int == 'muzza_ravioles':
									ravioles['muzza'] = (ravioles['muzza'] + line.product_uom_qty)
									total_ravioles = (total_ravioles + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'postre':
								if product_ref_int == 'am_c_dulce_de_leche_postre':
									postre['am_c_dulce_de_leche'] = (postre['am_c_dulce_de_leche'] + line.product_uom_qty)
									total_postre = (total_postre + line.product_uom_qty)
								elif product_ref_int == 'am_c_arandanos_postre':
									postre['am_c_arandanos'] = (postre['am_c_arandanos'] + line.product_uom_qty)
									total_postre = (total_postre + line.product_uom_qty)
								elif product_ref_int == 'choco_c_dulce_de_leche_postre':
									postre['choco_c_dulce_de_leche'] = (postre['choco_c_dulce_de_leche'] + line.product_uom_qty)
									total_postre = (total_postre + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'samosas_ch':
								if product_ref_int == 'papa_samosas_ch':
									samosas_ch['papa'] = (samosas_ch['papa'] + line.product_uom_qty)
									total_samosas_ch = (total_samosas_ch + line.product_uom_qty)
								elif product_ref_int == 'calabaza_samosas_ch':
									samosas_ch['calabaza'] = (samosas_ch['calabaza'] + line.product_uom_qty)
									total_samosas_ch = (total_samosas_ch + line.product_uom_qty)
								elif product_ref_int == 'batata_samosas_ch':
									samosas_ch['batata'] = (samosas_ch['batata'] + line.product_uom_qty)
									total_samosas_ch = (total_samosas_ch + line.product_uom_qty)
								elif product_ref_int == 'caprese_samosas_ch':
									samosas_ch['caprese'] = (samosas_ch['caprese'] + line.product_uom_qty)
									total_samosas_ch = (total_samosas_ch + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'frutas_gr':
								if product_ref_int == 'frambuesa_450g_frutas_gr':
									frutas_gr['frambuesa_450g'] = (frutas_gr['frambuesa_450g'] + line.product_uom_qty)
									total_frutas_gr = (total_frutas_gr + line.product_uom_qty)
								elif product_ref_int == 'arandano_600g_frutas_gr':
									frutas_gr['arandano_600g'] = (frutas_gr['arandano_600g'] + line.product_uom_qty)
									total_frutas_gr = (total_frutas_gr + line.product_uom_qty)
								elif product_ref_int	 == 'frutilla_600g_frutas_gr':
									frutas_gr['frutilla_600g'] = (frutas_gr['frutilla_600g'] + line.product_uom_qty)
									total_frutas_gr = (total_frutas_gr + line.product_uom_qty)
								elif product_ref_int == 'mix_berries_600g_frutas_gr':
									frutas_gr['mix_berries_600g'] = (frutas_gr['mix_berries_600g'] + line.product_uom_qty)
									total_frutas_gr = (total_frutas_gr + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'frutas_ch':
								if product_ref_int == 'frutilla_durazno_300g_frutas_ch':
									frutas_ch['frutilla_durazno_300g'] = (frutas_ch['frutilla_durazno_300g'] + line.product_uom_qty)
									total_frutas_ch = (total_frutas_ch + line.product_uom_qty)
								elif product_ref_int == 'mix_3_berries_300g_frutas_ch':
									frutas_ch['mix_3_berries_300g'] = (frutas_ch['mix_3_berries_300g'] + line.product_uom_qty)
									total_frutas_ch = (total_frutas_ch + line.product_uom_qty)
								elif product_ref_int == 'mango_maracuya_300g_frutas_ch':
									frutas_ch['mango_maracuya_300g'] = (frutas_ch['mango_maracuya_300g'] + line.product_uom_qty)
									total_frutas_ch = (total_frutas_ch + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'rebozados_kari':
								if product_ref_int == 'aros_rebozados_kari':
									rebozados_kari['aros'] = (rebozados_kari['aros'] + line.product_uom_qty)
									total_rebozados_kari = (total_rebozados_kari + line.product_uom_qty)
								elif product_ref_int == 'brocoli_rebozados_kari':
									rebozados_kari['brocoli'] = (rebozados_kari['brocoli'] + line.product_uom_qty)
									total_rebozados_kari = (total_rebozados_kari + line.product_uom_qty)
								elif product_ref_int == 'champi_rebozados_kari':
									rebozados_kari['champi'] = (rebozados_kari['champi'] + line.product_uom_qty)
									total_rebozados_kari = (total_rebozados_kari + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'bites':
								if product_ref_int == 'bites_arandanos_bites':
									bites['bites_arandanos'] = (bites['bites_arandanos'] + line.product_uom_qty)
									total_bites = (total_bites + line.product_uom_qty)
								elif product_ref_int == 'bites_frambuesas_bites':
									bites['bites_frambuesas'] = (bites['bites_frambuesas'] + line.product_uom_qty)
									total_bites = (total_bites + line.product_uom_qty)
								elif product_ref_int == 'bites_frutilla_bites':
									bites['bites_frutilla'] = (bites['bites_frutilla'] + line.product_uom_qty)
									total_bites = (total_bites + line.product_uom_qty)
								elif product_ref_int == 'calabaza_bites':
									bites['calabaza'] = (bites['calabaza'] + line.product_uom_qty)
									total_bites = (total_bites + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'torta':
								if product_ref_int == 'black_forest_torta':
									tortas['black_forest'] = (tortas['black_forest'] + line.product_uom_qty)
									total_torta = (total_torta + line.product_uom_qty)
								elif product_ref_int == 'blanco_y_frambuesa_torta':
									tortas['blanco_y_frambuesa'] = (tortas['blanco_y_frambuesa'] + line.product_uom_qty)
									total_torta = (total_torta + line.product_uom_qty)
								elif product_ref_int == 'marquise_torta':
									tortas['marquise'] = (tortas['marquise'] + line.product_uom_qty)
									total_torta = (total_torta + line.product_uom_qty)
								elif product_ref_int == 'nut_pie_torta':
									tortas['nut_pie'] = (tortas['nut_pie'] + line.product_uom_qty)
									total_torta = (total_torta + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'pizza':
								if product_ref_int == 'calabaza_pizza':
									pizza['calabaza'] = (pizza['calabaza'] + line.product_uom_qty)
									total_pizza = (total_pizza + line.product_uom_qty)
								elif product_ref_int == 'brocoli_pizza':
									pizza['brocoli'] = (pizza['brocoli'] + line.product_uom_qty)
									total_pizza = (total_pizza + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'pizza_veg':
								if product_ref_int == 'zanahoria_pizza_veg':
									pizza_veg['zanahoria'] = (pizza_veg['zanahoria'] + line.product_uom_qty)
									total_pizza_veg = (total_pizza_veg + line.product_uom_qty)
								elif product_ref_int == 'calabaza_pizza_veg':
									pizza_veg['calabaza'] = (pizza_veg['calabaza'] + line.product_uom_qty)
									total_pizza_veg = (total_pizza_veg + line.product_uom_qty)
								elif product_ref_int == 'brocoli_pizza_veg':
									pizza_veg['brocoli'] = (pizza_veg['brocoli'] + line.product_uom_qty)
									total_pizza_veg = (total_pizza_veg + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'croqueta':
								if product_ref_int == 'espinaca_croqueta':
									croqueta['espinaca'] = (croqueta['espinaca'] + line.product_uom_qty)
									total_croqueta = (total_croqueta + line.product_uom_qty)
								elif product_ref_int == 'calabaza_croqueta':
									croqueta['calabaza'] = (croqueta['calabaza'] + line.product_uom_qty)
									total_croqueta = (total_croqueta + line.product_uom_qty)
								elif product_ref_int == 'batata_croqueta':
									croqueta['batata'] = (croqueta['batata'] + line.product_uom_qty)
									total_croqueta = (total_croqueta + line.product_uom_qty)
								elif product_ref_int == 'papa_croqueta':
									croqueta['papa'] = (croqueta['papa'] + line.product_uom_qty)
									total_croqueta = (total_croqueta + line.product_uom_qty)
								elif product_ref_int == 'espi_veg_croqueta':
									croqueta['espi_veg'] = (croqueta['espi_veg'] + line.product_uom_qty)
									total_croqueta = (total_croqueta + line.product_uom_qty)
								elif product_ref_int == 'calabaza_veg_croqueta':
									croqueta['calabaza_veg'] = (croqueta['calabaza_veg'] + line.product_uom_qty)
									total_croqueta = (total_croqueta + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'station':
								if product_ref_int == 'bocadito_station':
									station['bocadito'] = (station['bocadito'] + line.product_uom_qty)
									total_station = (total_station + line.product_uom_qty)
								elif product_ref_int == 'caprese_station':
									station['caprese'] = (station['caprese'] + line.product_uom_qty)
									total_station = (total_station + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'kari_yogt_ch':
								if product_ref_int == 'choconut_kari_yogt_ch':
									kari_yogt_ch['choconut'] = (kari_yogt_ch['choconut'] + line.product_uom_qty)
									total_kari_yogt_ch = (total_kari_yogt_ch + line.product_uom_qty)
								elif product_ref_int == 'choco_amargo_kari_yogt_ch':
									kari_yogt_ch['choco_amargo'] = (kari_yogt_ch['choco_amargo'] + line.product_uom_qty)
									total_kari_yogt_ch = (total_kari_yogt_ch + line.product_uom_qty)
								elif product_ref_int == 'dulce_de_leche_kari_yogt_ch':
									kari_yogt_ch['dulce_de_leche'] = (kari_yogt_ch['dulce_de_leche'] + line.product_uom_qty)
									total_kari_yogt_ch = (total_kari_yogt_ch + line.product_uom_qty)
								elif product_ref_int == 'frutilla_kari_yogt_ch':
									kari_yogt_ch['frutilla'] = (kari_yogt_ch['frutilla'] + line.product_uom_qty)
									total_kari_yogt_ch = (total_kari_yogt_ch + line.product_uom_qty)
								elif product_ref_int == 'frutos_del_bosque_kari_yogt_ch':
									kari_yogt_ch['frutos_del_bosque'] = (kari_yogt_ch['frutos_del_bosque'] + line.product_uom_qty)
									total_kari_yogt_ch = (total_kari_yogt_ch + line.product_uom_qty)
								elif product_ref_int == 'maracuya_kari_yogt_ch':
									kari_yogt_ch['maracuya'] = (kari_yogt_ch['maracuya'] + line.product_uom_qty)
									total_kari_yogt_ch = (total_kari_yogt_ch + line.product_uom_qty)
								elif product_ref_int == 'griego_kari_yogt_ch':
									kari_yogt_ch['griego'] = (kari_yogt_ch['griego'] + line.product_uom_qty)
									total_kari_yogt_ch = (total_kari_yogt_ch + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'kari_yogt_gr':
								if product_ref_int == 'frutos_del_bosque_kari_yogt_gr':
									kari_yogt_gr['frutos_del_bosque'] = (kari_yogt_gr['frutos_del_bosque'] + line.product_uom_qty)
									total_kari_yogt_gr = (total_kari_yogt_gr + line.product_uom_qty)
								elif product_ref_int == 'maracuya_kari_yogt_gr':
									kari_yogt_gr['maracuya'] = (kari_yogt_gr['maracuya'] + line.product_uom_qty)
									total_kari_yogt_gr = (total_kari_yogt_gr + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'amoedo_tarta':
								if product_ref_int == 'cala_amoedo_tarta':
									amoedo_tarta['cala'] = (amoedo_tarta['cala'] + line.product_uom_qty)
									total_amoedo_tarta = (total_amoedo_tarta + line.product_uom_qty)
								elif product_ref_int == 'cebo_amoedo_tarta':
									amoedo_tarta['cebo'] = (amoedo_tarta['cebo'] + line.product_uom_qty)
									total_amoedo_tarta = (total_amoedo_tarta + line.product_uom_qty)
								elif product_ref_int == 'caprese_amoedo_tarta':
									amoedo_tarta['caprese'] = (amoedo_tarta['caprese'] + line.product_uom_qty)
									total_amoedo_tarta = (total_amoedo_tarta + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'amoedo_integral':
								if product_ref_int == 'cala_amoedo_integral':
									amoedo_integral['cala'] = (amoedo_integral['cala'] + line.product_uom_qty)
									total_amoedo_integral = (total_amoedo_integral + line.product_uom_qty)
								elif product_ref_int == 'zana_amoedo_integral':
									amoedo_integral['zana'] = (amoedo_integral['zana'] + line.product_uom_qty)
									total_amoedo_integral = (total_amoedo_integral + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

						report_has_congelados = True
					elif categ_ecomm == 'refrigerados':
						if line.product_id.categ_id:
							categ_int = None
							product_ref_int = line.product_id.default_code
							if ' ' in line.product_id.categ_id.name:
								str_replace = line.product_id.categ_id.name.lower().split(' ')
								if len(str_replace) == 3:
									categ_int = "%s_%s_%s" %(str_replace[0], str_replace[1], str_replace[2])
								else:
									categ_int = "%s_%s" %(str_replace[0], str_replace[1])
							else:
								categ_int = line.product_id.categ_id.name.lower()
							if categ_int == 'casa_vegana':
								if product_ref_int == 'aduki_hungaro_casa_vegana':
									casa_vegana['aduki_hungaro'] = (casa_vegana['aduki_hungaro'] + line.product_uom_qty)
									total_casa_vegana = (total_casa_vegana + line.product_uom_qty)
								elif product_ref_int == 'aduki_remolacha_casa_vegana':
									casa_vegana['aduki_remolacha'] = (casa_vegana['aduki_remolacha'] + line.product_uom_qty)
									total_casa_vegana = (total_casa_vegana + line.product_uom_qty)
								elif product_ref_int == 'green_moon_casa_vegana':
									casa_vegana['green_moon'] = (casa_vegana['green_moon'] + line.product_uom_qty)
									total_casa_vegana = (total_casa_vegana + line.product_uom_qty)
								elif product_ref_int == 'lentejon_casa_vegana':
									casa_vegana['lentejon'] = (casa_vegana['lentejon'] + line.product_uom_qty)
									total_casa_vegana = (total_casa_vegana + line.product_uom_qty)
								elif product_ref_int == 'mijo_casa_vegana':
									casa_vegana['mijo'] = (casa_vegana['mijo'] + line.product_uom_qty)
									total_casa_vegana = (total_casa_vegana + line.product_uom_qty)
								elif product_ref_int == 'quinoa_andina_casa_vegana':
									casa_vegana['quinoa_andina'] = (casa_vegana['quinoa_andina'] + line.product_uom_qty)
									total_casa_vegana = (total_casa_vegana + line.product_uom_qty)
								elif product_ref_int == 'quinoa_hindu_casa_vegana':
									casa_vegana['quinoa_hindu'] = (casa_vegana['quinoa_hindu'] + line.product_uom_qty)
									total_casa_vegana = (total_casa_vegana + line.product_uom_qty)
								elif product_ref_int == 'quinoa_mediterranea_casa_vegana':
									casa_vegana['quinoa_mediterranea'] = (casa_vegana['quinoa_mediterranea'] + line.product_uom_qty)
									total_casa_vegana = (total_casa_vegana + line.product_uom_qty)
								elif product_ref_int == 'quinoa_sin_sal_casa_vegana':
									casa_vegana['quinoa_sin_sal'] = (casa_vegana['quinoa_sin_sal'] + line.product_uom_qty)
									total_casa_vegana = (total_casa_vegana + line.product_uom_qty)
								elif product_ref_int == 'yamani_casa_vegana':
									casa_vegana['yamani'] = (casa_vegana['yamani'] + line.product_uom_qty)
									total_casa_vegana = (total_casa_vegana + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'casa_vegana_toq':
								if product_ref_int == 'falafel_casa_vegana_toq':
									casa_vegana_toq['falafel'] = (casa_vegana_toq['falafel'] + line.product_uom_qty)
									total_casa_vegana_toq = (total_casa_vegana_toq + line.product_uom_qty)
								elif product_ref_int == 'nugget_casa_vegana_toq':
									casa_vegana_toq['nugget'] = (casa_vegana_toq['nugget'] + line.product_uom_qty)
									total_casa_vegana_toq = (total_casa_vegana_toq + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'vivet_leche':
								if product_ref_int == 'cafe_latte_vivet_leche':
									vivet_leche['cafe_latte'] = (vivet_leche['cafe_latte'] + line.product_uom_qty)
									total_vivet_leche = (total_vivet_leche + line.product_uom_qty)
								elif product_ref_int == 'chocolate_vivet_leche':
									vivet_leche['chocolate'] = (vivet_leche['chocolate'] + line.product_uom_qty)
									total_vivet_leche = (total_vivet_leche + line.product_uom_qty)
								elif product_ref_int == 'frutilla_vivet_leche':
									vivet_leche['frutilla'] = (vivet_leche['frutilla'] + line.product_uom_qty)
									total_vivet_leche = (total_vivet_leche + line.product_uom_qty)
								elif product_ref_int == 'original_vivet_leche':
									vivet_leche['original'] = (vivet_leche['original'] + line.product_uom_qty)
									total_vivet_leche = (total_vivet_leche + line.product_uom_qty)
								elif product_ref_int == 'vainilla_vivet_leche':
									vivet_leche['vainilla'] = (vivet_leche['vainilla'] + line.product_uom_qty)
									total_vivet_leche = (total_vivet_leche + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'vivet_queso':
								if product_ref_int == 'fina_hierbas_vivet_queso':
									vivet_queso['fina_hierbas'] = (vivet_queso['fina_hierbas'] + line.product_uom_qty)
									total_vivet_queso = (total_vivet_queso + line.product_uom_qty)
								elif product_ref_int == 'natural_vivet_queso':
									vivet_queso['natural'] = (vivet_queso['natural'] + line.product_uom_qty)
									total_vivet_queso = (total_vivet_queso + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'sirius':
								if product_ref_int == 'sirius_sirius':
									sirius['sirius'] = (sirius['sirius'] + line.product_uom_qty)
									total_sirius = (total_sirius + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'placer':
								if product_ref_int == 'vainilla_placer':
									placer['vainilla'] = (placer['vainilla'] + line.product_uom_qty)
									total_placer = (total_placer + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'quimya':
								if product_ref_int == 'arandanos_quimya':
									quimya['arandanos'] = (quimya['arandanos'] + line.product_uom_qty)
									total_quimya = (total_quimya + line.product_uom_qty)
								elif product_ref_int == 'chocolate_quimya':
									quimya['chocolate'] = (quimya['chocolate'] + line.product_uom_qty)
									total_quimya = (total_quimya + line.product_uom_qty)
								if product_ref_int == 'coconut_quimya':
									quimya['coconut'] = (quimya['coconut'] + line.product_uom_qty)
									total_quimya = (total_quimya + line.product_uom_qty)
								elif product_ref_int == 'frutilla_quimya':
									quimya['frutilla'] = (quimya['frutilla'] + line.product_uom_qty)
									total_quimya = (total_quimya + line.product_uom_qty)
								if product_ref_int == 'keylime_palta_granola__quimya':
									quimya['keylime_palta_granola'] = (quimya['keylime_palta_granola'] + line.product_uom_qty)
									total_quimya = (total_quimya + line.product_uom_qty)
								elif product_ref_int == 'mango_quimya':
									quimya['mango'] = (quimya['mango'] + line.product_uom_qty)
									total_quimya = (total_quimya + line.product_uom_qty)
								if product_ref_int == 'natural_con_granola_quimya':
									quimya['natural_con_granola'] = (quimya['natural_con_granola'] + line.product_uom_qty)
									total_quimya = (total_quimya + line.product_uom_qty)
								elif product_ref_int == 'vainilla_quimya':
									quimya['vainilla'] = (quimya['vainilla'] + line.product_uom_qty)
									total_quimya = (total_quimya + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'fv_cheddar':
								if product_ref_int == 'cheddar_fv_cheddar':
									fv_cheddar['cheddar'] = (fv_cheddar['cheddar'] + line.product_uom_qty)
									total_fv_cheddar = (total_fv_cheddar + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'fv_provoleta':
								if product_ref_int == 'provoleta_fv_provoleta':
									fv_provoleta['provoleta'] = (fv_provoleta['provoleta'] + line.product_uom_qty)
									total_fv_provoleta = (total_fv_provoleta + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'fv_hummus':
								if product_ref_int == 'hummus_fv_hummus':
									fv_hummus['hummus'] = (fv_hummus['hummus'] + line.product_uom_qty)
									total_fv_hummus = (total_fv_hummus + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int =='fv_yogurt':
								if product_ref_int == 'yogurt_cereales_fv_yogurt':
									fv_yogurt['yogurt_cereales'] = (fv_yogurt['yogurt_cereales'] + line.product_uom_qty)
									total_fv_yogurt = (total_fv_yogurt + line.product_uom_qty)
								elif product_ref_int == 'yogurt_durazno_fv_yogurt':
									fv_yogurt['yogurt_durazno'] = (fv_yogurt['yogurt_durazno'] + line.product_uom_qty)
									total_fv_yogurt = (total_fv_yogurt + line.product_uom_qty)
								elif product_ref_int == 'yogurt_frutilla_fv_yogurt':
									fv_yogurt['yogurt_frutilla'] = (fv_yogurt['yogurt_frutilla'] + line.product_uom_qty)
									total_fv_yogurt = (total_fv_yogurt + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'fv_dulce_ch':
								if product_ref_int == 'dulce_ch_fv_dulce_ch':
									fv_dulce_ch['dulce_ch'] = (fv_dulce_ch['dulce_ch'] + line.product_uom_qty)
									total_fv_dulce_ch = (total_fv_dulce_ch + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'fv_dulce_gr':
								if product_ref_int == 'dulce_gr_fv_dulce_gr':
									fv_dulce_gr['dulce_gr'] = (fv_dulce_gr['dulce_gr'] + line.product_uom_qty)
									total_fv_dulce_gr = (total_fv_dulce_gr + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'fv_alfajor':
								if product_ref_int == 'alfajor_chocolate_fv_alfajor':
									fv_alfajor['alfajor_chocolate'] = (fv_alfajor['alfajor_chocolate'] + line.product_uom_qty)
									total_fv_alfajor = (total_fv_alfajor + line.product_uom_qty)
								if product_ref_int == 'alfajor_maicena_fv_alfajor':
									fv_alfajor['alfajor_maicena'] = (fv_alfajor['alfajor_maicena'] + line.product_uom_qty)
									total_fv_alfajor = (total_fv_alfajor + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'logo':
								if product_ref_int == 'logo_arandanos_logo':
									logo['logo_arandanos'] = (logo['logo_arandanos'] + line.product_uom_qty)
									total_logo = (total_logo + line.product_uom_qty)
								elif product_ref_int == 'logo_durazno_s_azucar_logo':
									logo['logo_durazno_s_azucar'] = (logo['logo_durazno_s_azucar'] + line.product_uom_qty)
									total_logo = (total_logo + line.product_uom_qty)
								elif product_ref_int == 'logo_frutilla_logo':
									logo['logo_frutilla'] = (logo['logo_frutilla'] + line.product_uom_qty)
									total_logo = (total_logo + line.product_uom_qty)
								elif product_ref_int == 'logo_frutilla_s_azucar_logo':
									logo['logo_frutilla_s_azucar'] = (logo['logo_frutilla_s_azucar'] + line.product_uom_qty)
									total_logo = (total_logo + line.product_uom_qty)
								elif product_ref_int == 'logo_maracuya_logo':
									logo['logo_maracuya'] = (logo['logo_maracuya'] + line.product_uom_qty)
									total_logo = (total_logo + line.product_uom_qty)
								elif product_ref_int == 'logo_natural_granola_logo':
									logo['logo_natural_granola'] = (logo['logo_natural_granola'] + line.product_uom_qty)
									total_logo = (total_logo + line.product_uom_qty)
								elif product_ref_int == 'logo_natural_logo':
									logo['logo_natural'] = (logo['logo_natural'] + line.product_uom_qty)
									total_logo = (total_logo + line.product_uom_qty)
								elif product_ref_int == 'logo_vainilla_granola_logo':
									logo['logo_vainilla_granola'] = (logo['logo_vainilla_granola'] + line.product_uom_qty)
									total_logo = (total_logo + line.product_uom_qty)
								elif product_ref_int == 'logo_vainilla_logo':
									logo['logo_vainilla'] = (logo['logo_vainilla'] + line.product_uom_qty)
									total_logo = (total_logo + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'cudda_hormita':
								if product_ref_int == 'crudda_ahumado_cudda_hormita':
									cudda_hormita['crudda_ahumado'] = (cudda_hormita['crudda_ahumado'] + line.product_uom_qty)
									total_cudda_hormita = (total_cudda_hormita + line.product_uom_qty)
								elif product_ref_int == 'crudda_clasico_cudda_hormita':
									cudda_hormita['crudda_clasico'] = (cudda_hormita['crudda_clasico'] + line.product_uom_qty)
									total_cudda_hormita = (total_cudda_hormita + line.product_uom_qty)
								elif product_ref_int == 'crudda_pimienta_cudda_hormita':
									cudda_hormita['crudda_pimienta'] = (cudda_hormita['crudda_pimienta'] + line.product_uom_qty)
									total_cudda_hormita = (total_cudda_hormita + line.product_uom_qty)
								elif product_ref_int == 'crudda_provence_cudda_hormita':
									cudda_hormita['crudda_provence'] = (cudda_hormita['crudda_provence'] + line.product_uom_qty)
									total_cudda_hormita = (total_cudda_hormita + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'cudda_untable':
								if product_ref_int == 'crudda_untable_cudda_untable':
									cudda_untable['crudda_untable'] = (cudda_hormita['crudda_untable'] + line.product_uom_qty)
									total_cudda_untable = (total_cudda_untable + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'nina':
								if product_ref_int == 'blondies_nina_refr':
									nina_refr['blondies'] = (nina_refr['blondies'] + line.product_uom_qty)
									total_nina_refr = (total_nina_refr + line.product_uom_qty)
								elif product_ref_int == 'chocochips_nina_refr':
									nina_refr['chocochips'] = (nina_refr['chocochips'] + line.product_uom_qty)
									total_nina_refr = (total_nina_refr + line.product_uom_qty)
								elif product_ref_int == 'chocolate_nina_refr':
									nina_refr['chocolate'] = (nina_refr['chocolate'] + line.product_uom_qty)
									total_nina_refr = (total_nina_refr + line.product_uom_qty)
								elif product_ref_int == 'cranberry_nina_refr':
									nina_refr['cranberry'] = (nina_refr['cranberry'] + line.product_uom_qty)
									total_nina_refr = (total_nina_refr + line.product_uom_qty)
								elif product_ref_int == 'biscochitos_nina_refr':
									nina_refr['biscochitos'] = (nina_refr['biscochitos'] + line.product_uom_qty)
									total_nina_refr = (total_nina_refr + line.product_uom_qty)
								elif product_ref_int == 'sugar_limon_nina_refr':
									nina_refr['sugar_limon'] = (nina_refr['sugar_limon'] + line.product_uom_qty)
									total_nina_refr = (total_nina_refr + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'quimya_yog':
								if product_ref_int == 'untable_felicia_quimya_yog':
									quimya_yog['untable_felicia'] = (quimya_yog['untable_felicia'] + line.product_uom_qty)
									total_quimya_yog = (total_quimya_yog + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'augus_untable':
								if product_ref_int == 'clasico_augus_untable':
									augus_untable['clasico'] = (augus_untable['clasico'] + line.product_uom_qty)
									total_augus_untable = (total_augus_untable + line.product_uom_qty)
								elif product_ref_int == 'ciboulette_augus_untable':
									augus_untable['ciboulette'] = (augus_untable['ciboulette'] + line.product_uom_qty)
									total_augus_untable = (total_augus_untable + line.product_uom_qty)
								elif product_ref_int == 'pimenton_augus_untable':
									augus_untable['pimenton'] = (augus_untable['pimenton'] + line.product_uom_qty)
									total_augus_untable = (total_augus_untable + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'augus_horma':
								if product_ref_int == 'clasica_augus_horma':
									augus_horma['clasica'] = (augus_horma['clasica'] + line.product_uom_qty)
									total_augus_horma = (total_augus_horma + line.product_uom_qty)
								elif product_ref_int == 'hierbas_augus_horma':
									augus_horma['hierbas'] = (augus_horma['hierbas'] + line.product_uom_qty)
									total_augus_horma = (total_augus_horma + line.product_uom_qty)
								elif product_ref_int == 'camembert_augus_horma':
									augus_horma['camembert'] = (augus_horma['camembert'] + line.product_uom_qty)
									total_augus_horma = (total_augus_horma + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'kombucha':
								if product_ref_int == 'verde_kombucha_refr':
									kombucha_refr['verde'] = (kombucha_refr['verde'] + line.product_uom_qty)
									total_kombucha_refr = (total_kombucha_refr + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'fv_botell_ch':
								if product_ref_int == 'leche_almendra_fv_botell_ch':
									fv_botell_ch['leche_almendra'] = (fv_botell_ch['leche_almendra'] + line.product_uom_qty)
									total_fv_botell_ch = (total_fv_botell_ch + line.product_uom_qty)
								elif product_ref_int == 'leche_chocolatada_fv_botell_ch':
									fv_botell_ch['leche_chocolatada'] = (fv_botell_ch['leche_chocolatada'] + line.product_uom_qty)
									total_fv_botell_ch = (total_fv_botell_ch + line.product_uom_qty)
								elif product_ref_int == 'leche_coco_fv_botell_ch':
									fv_botell_ch['leche_coco'] = (fv_botell_ch['leche_coco'] + line.product_uom_qty)
									total_fv_botell_ch = (total_fv_botell_ch + line.product_uom_qty)
								elif product_ref_int == 'smoothie_frutos_fv_botell_ch':
									fv_botell_ch['smoothie_frutos'] = (fv_botell_ch['smoothie_frutos'] + line.product_uom_qty)
									total_fv_botell_ch = (total_fv_botell_ch + line.product_uom_qty)
								elif product_ref_int == 'smoothie_mango_fv_botell_ch':
									fv_botell_ch['smoothie_mango'] = (fv_botell_ch['smoothie_mango'] + line.product_uom_qty)
									total_fv_botell_ch = (total_fv_botell_ch + line.product_uom_qty)
								elif product_ref_int == 'smoothie_banana_fv_botell_ch':
									fv_botell_ch['smoothie_banana'] = (fv_botell_ch['smoothie_banana'] + line.product_uom_qty)
									total_fv_botell_ch = (total_fv_botell_ch + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'fv_crema':
								if product_ref_int == 'crema_fv_crema':
									fv_crema['crema'] = (fv_crema['crema'] + line.product_uom_qty)
									total_fv_crema = (total_fv_crema + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'jugo_litro':
								if product_ref_int == 'rojo_jugo_litro':
									jugo_litro['rojo'] = (jugo_litro['rojo'] + line.product_uom_qty)
									total_jugo_litro = (total_jugo_litro + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'cacah_vivet':
								if product_ref_int == 'vainilla_cacah_vivet':
									cacah_vivet['vainilla'] = (cacah_vivet['vainilla'] + line.product_uom_qty)
									total_cacah_vivet = (total_cacah_vivet + line.product_uom_qty)
								elif product_ref_int == 'choco_cacah_vivet':
									cacah_vivet['choco'] = (cacah_vivet['choco'] + line.product_uom_qty)
									total_cacah_vivet = (total_cacah_vivet + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'notco':
								if product_ref_int == 'mayo_notco':
									notco['mayo'] = (notco['mayo'] + line.product_uom_qty)
									total_notco = (total_notco + line.product_uom_qty)
								elif product_ref_int == 'notmilk_notco':
									notco['notmilk'] = (notco['notmilk'] + line.product_uom_qty)
									total_notco = (total_notco + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'silk':
								if product_ref_int == 'almendra_silk':
									silk_refr['almendra'] = (silk_refr['almendra'] + line.product_uom_qty)
									total_silk_refr = (total_silk_refr + line.product_uom_qty)
								elif product_ref_int == 's_azucar_silk':
									silk_refr['s_azucar'] = (silk_refr['s_azucar'] + line.product_uom_qty)
									total_silk_refr = (total_silk_refr + line.product_uom_qty)
								elif product_ref_int == 'coco_silk':
									silk_refr['coco'] = (silk_refr['coco'] + line.product_uom_qty)
									total_silk_refr = (total_silk_refr + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'dale_coco':
								if product_ref_int == 'leche_de_coco_dale_coco':
									dale_coco_refr['leche_de_coco'] = (dale_coco_refr['leche_de_coco'] + line.product_uom_qty)
									total_dale_coco_refr = (total_dale_coco_refr + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'sonder':
								if product_ref_int == 'green_tree_sonder':
									sonder['green_tree'] = (sonder['green_tree'] + line.product_uom_qty)
									total_sonder = (total_sonder + line.product_uom_qty)
								elif product_ref_int == 'sunrise_coco_sonder':
									sonder['sunrise'] = (sonder['sunrise'] + line.product_uom_qty)
									total_sonder = (total_sonder + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

						report_has_refrigerados = True
					elif categ_ecomm == 'secos':
						if line.product_id.categ_id:
							categ_int = None
							product_ref_int = line.product_id.default_code
							if ' ' in line.product_id.categ_id.name:
								str_replace = line.product_id.categ_id.name.lower().split(' ')
								if len(str_replace) == 3:
									categ_int = "%s_%s_%s" %(str_replace[0], str_replace[1], str_replace[2])
								else:
									categ_int = "%s_%s" %(str_replace[0], str_replace[1])
							else:
								categ_int = line.product_id.categ_id.name.lower()

							if categ_int == 'vivet_cacahuate':
								if product_ref_int == 'cacao_vivet_cacahuate':
									vivet_cacahuate['cacao'] = (vivet_cacahuate['cacao'] + line.product_uom_qty)
									total_vivet_cacahuate = (total_vivet_cacahuate + line.product_uom_qty)
								elif product_ref_int == 'vainilla_caramel_vivet_cacahuate':
									vivet_cacahuate['vainilla_caramel'] = (vivet_cacahuate['vainilla_caramel'] + line.product_uom_qty)
									total_vivet_cacahuate = (total_vivet_cacahuate + line.product_uom_qty)
								elif product_ref_int == 'vainilla_natural_vivet_cacahuate':
									vivet_cacahuate['vainilla_natural'] = (vivet_cacahuate['vainilla_natural'] + line.product_uom_qty)
									total_vivet_cacahuate = (total_vivet_cacahuate + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'quimya_granola':
								if product_ref_int == 'familiar_quimya_granola':
									quimya_granola['familiar'] = (quimya_granola['familiar'] + line.product_uom_qty)
									total_quimya_granola = (total_quimya_granola + line.product_uom_qty)
								elif product_ref_int == 'individual_quimya_granola':
									quimya_granola['individual'] = (quimya_granola['individual'] + line.product_uom_qty)
									total_quimya_granola = (total_quimya_granola + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'kombucha':
								if product_ref_int == 'negro_kombucha':
									kombucha['negro'] = (kombucha['negro'] + line.product_uom_qty)
									total_kombucha = (total_kombucha + line.product_uom_qty)
								elif product_ref_int == 'rojo_kombucha':
									kombucha['rojo'] = (kombucha['rojo'] + line.product_uom_qty)
									total_kombucha = (total_kombucha + line.product_uom_qty)
								elif product_ref_int == 'verde_kombucha':
									kombucha['verde'] = (kombucha['verde'] + line.product_uom_qty)
									total_kombucha = (total_kombucha + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'felices_alfajor':
								if product_ref_int == 'chocolate_felices_alfajor':
									felices_alfajor['chocolate'] = (felices_alfajor['chocolate'] + line.product_uom_qty)
									total_felices_alfajor = (total_felices_alfajor + line.product_uom_qty)
								elif product_ref_int == 'maicena_felices_alfajor':
									felices_alfajor['maicena'] = (felices_alfajor['maicena'] + line.product_uom_qty)
									total_felices_alfajor = (total_felices_alfajor + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'nina':
								if product_ref_int == 'bizcochitos_nina_sec':
									nina_sec['bizcochitos'] = (nina_sec['bizcochitos'] + line.product_uom_qty)
									total_nina_sec = (total_nina_sec + line.product_uom_qty)
								elif product_ref_int == 'blondie_nina_sec':
									nina_sec['blondie'] = (nina_sec['blondie'] + line.product_uom_qty)
									total_nina_sec = (total_nina_sec + line.product_uom_qty)
								elif product_ref_int == 'blondies_sugar_free_nina_sec':
									nina_sec['blondies_sugar_free'] = (nina_sec['blondies_sugar_free'] + line.product_uom_qty)
									total_nina_sec = (total_nina_sec + line.product_uom_qty)
								elif product_ref_int == 'chocochips_nina_sec':
									nina_sec['chocochips'] = (nina_sec['chocochips'] + line.product_uom_qty)
									total_nina_sec = (total_nina_sec + line.product_uom_qty)
								elif product_ref_int == 'choco_nina_sec':
									nina_sec['choco'] = (nina_sec['choco'] + line.product_uom_qty)
									total_nina_sec = (total_nina_sec + line.product_uom_qty)
								elif product_ref_int == 'cranberry_nina_sec':
									nina_sec['cranberry'] = (nina_sec['cranberry'] + line.product_uom_qty)
									total_nina_sec = (total_nina_sec + line.product_uom_qty)
								elif product_ref_int == 'limon_nina_sec':
									nina_sec['limon'] = (nina_sec['limon'] + line.product_uom_qty)
									total_nina_sec = (total_nina_sec + line.product_uom_qty)
								elif product_ref_int == 'limon_sugar_free_nina_sec':
									nina_sec['limon_sugar_free'] = (nina_sec['limon_sugar_free'] + line.product_uom_qty)
									total_nina_sec = (total_nina_sec + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'pf_litro':
								if product_ref_int == 'arandanos_pf_litro':
									pf_litro['arandanos'] = (pf_litro['arandanos'] + line.product_uom_qty)
									total_pf_litro = (total_pf_litro + line.product_uom_qty)
								elif product_ref_int == 'frutilla_pf_litro':
									pf_litro['frutilla'] = (pf_litro['frutilla'] + line.product_uom_qty)
									total_pf_litro = (total_pf_litro + line.product_uom_qty)
								elif product_ref_int == 'kiwi_pf_litro':
									pf_litro['kiwi'] = (pf_litro['kiwi'] + line.product_uom_qty)
									total_pf_litro = (total_pf_litro + line.product_uom_qty)
								elif product_ref_int == 'manzana_roja_pf_litro':
									pf_litro['manzana_roja'] = (pf_litro['manzana_roja'] + line.product_uom_qty)
									total_pf_litro = (total_pf_litro + line.product_uom_qty)
								elif product_ref_int == 'manzana_verde_pf_litro':
									pf_litro['manzana_verde'] = (pf_litro['manzana_verde'] + line.product_uom_qty)
									total_pf_litro = (total_pf_litro + line.product_uom_qty)
								elif product_ref_int == 'naranja_pf_litro':
									pf_litro['naranja'] = (pf_litro['naranja'] + line.product_uom_qty)
									total_pf_litro = (total_pf_litro + line.product_uom_qty)
								elif product_ref_int == 'organico_pf_litro':
									pf_litro['organico'] = (pf_litro['organico'] + line.product_uom_qty)
									total_pf_litro = (total_pf_litro + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'pf_500ml':
								if product_ref_int == 'manzana_roja_pf_500ml':
									pf_500ml['manzana_roja'] = (pf_500ml['manzana_roja'] + line.product_uom_qty)
									total_pf_500ml = (total_pf_500ml + line.product_uom_qty)
								elif product_ref_int == 'manzana_verde_pf_500ml':
									pf_500ml['manzana_verde'] = (pf_500ml['manzana_verde'] + line.product_uom_qty)
									total_pf_500ml = (total_pf_500ml + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'pf_330ml':
								if product_ref_int == 'naranja_pf_330ml':
									pf_330ml['naranja'] = (pf_330ml['naranja'] + line.product_uom_qty)
									total_pf_330ml = (total_pf_330ml + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'pf_200ml':
								if product_ref_int == 'manzana_roja_pf_200ml':
									pf_200ml['manzana_roja'] = (pf_200ml['manzana_roja'] + line.product_uom_qty)
									total_pf_200ml = (total_pf_200ml + line.product_uom_qty)
								elif product_ref_int == 'manzana_verde_pf_200ml':
									pf_200ml['manzana_verde'] = (pf_200ml['manzana_verde'] + line.product_uom_qty)
									total_pf_200ml = (total_pf_200ml + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'notmayo':
								if product_ref_int == 'mayonesa_notmayo':
									notmayo['mayonesa'] = (notmayo['mayonesa'] + line.product_uom_qty)
									total_notmayo = (total_notmayo + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'notmilk':
								if product_ref_int == 'not_milk_notmilk':
									notmilk['not_milk'] = (notmilk['not_milk'] + line.product_uom_qty)
									total_notmilk = (total_notmilk + line.product_uom_qty)
								elif product_ref_int == 'promocion_notmilk':
									notmilk['promocion'] = (notmilk['promocion'] + line.product_uom_qty)
									total_notmilk = (total_notmilk + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'silk':
								if product_ref_int == 'almendra_silk':
									silk['almendra'] = (silk['almendra'] + line.product_uom_qty)
									total_silk = (total_silk + line.product_uom_qty)
								elif product_ref_int == 'almendra_sin_azucar_silk':
									silk['almendra_sin_azucar'] = (silk['almendra_sin_azucar'] + line.product_uom_qty)
									total_silk = (total_silk + line.product_uom_qty)
								elif product_ref_int == 'alm_vainilla_silk':
									silk['alm_vainilla'] = (silk['alm_vainilla'] + line.product_uom_qty)
									total_silk = (total_silk + line.product_uom_qty)
								elif product_ref_int == 'chocolatada_silk':
									silk['chocolatada'] = (silk['chocolatada'] + line.product_uom_qty)
									total_silk = (total_silk + line.product_uom_qty)
								elif product_ref_int == 'coco_silk':
									silk['coco'] = (silk['coconut'] + line.product_uom_qty)
									total_silk = (total_silk + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

							elif categ_int == 'dale_coco':
								if product_ref_int == 'agua_de_coco_dale_coco':
									dale_coco['agua_de_coco'] = (dale_coco['agua_de_coco'] + line.product_uom_qty)
									total_dale_coco = (total_dale_coco + line.product_uom_qty)
								elif product_ref_int == 'leche_de_coco_dale_coco':
									dale_coco['leche_de_coco'] = (dale_coco['leche_de_coco'] + line.product_uom_qty)
									total_dale_coco = (total_dale_coco + line.product_uom_qty)
								else:
									_logger.info('%s no registrada en la lista' % (categ_int))

						report_has_secos = True
					else:
						_logger.info('sin categoria ecommerce')

			if report_has_congelados is True:
				dict_so['categories'].append({'congelados': {
					'date_order': date_order,
					'name': name,
					'burganas': burganas,
					'caja_burganas': caja_burganas,
					'haulani_180': haulani_180,
					'haulani_500': haulani_500,
					'kaira_cla_250': kaira_cla_250,
					'kaira_liv_500': kaira_liv_500,
					'kaira_liv_250': kaira_liv_250,
					'kaira_liv_120': kaira_liv_120,
					'ravioles': ravioles,
					'postre': postre,
					'samosas_ch': samosas_ch,
					'pizza': pizza,
					'pizza_veg': pizza_veg,
					'croqueta': croqueta,
					'station': station,
					'kari_yogt_ch': kari_yogt_ch,
					'kari_yogt_gr': kari_yogt_gr,
					'amoedo_tarta': amoedo_tarta,
					'amoedo_integral': amoedo_integral,
					'frutas_gr': frutas_gr,
					'frutas_ch': frutas_ch,
					'rebozados_kari': rebozados_kari,
					'bites': bites,
					'tortas': tortas,
					'total_burganas': total_burganas,
					'total_caja_burganas':  total_caja_burganas,
					'total_frutas_gr': total_frutas_gr,
					'total_frutas_ch': total_frutas_ch,
					'total_rebozados_kari': total_rebozados_kari,
					'total_bites': total_bites,
					'total_torta': total_torta,
					'total_haulani_180': total_haulani_180,
					'total_haulani_500': total_haulani_500,
					'total_kaira_cla_250': total_kaira_cla_250,
					'total_kaira_liv_500': total_kaira_liv_500,
					'total_kaira_liv_250': total_kaira_liv_250,
					'total_kaira_liv_120': total_kaira_liv_120,
					'total_ravioles': total_ravioles,
					'total_postre': total_postre,
					'total_samosas_ch': total_samosas_ch,
					'total_pizza': total_pizza,
					'total_pizza_veg': total_pizza_veg,
					'total_croqueta': total_croqueta,
					'total_station': total_station,
					'total_kari_yogt_ch': total_kari_yogt_ch,
					'total_kari_yogt_gr': total_kari_yogt_gr,
					'total_amoedo_tarta': total_amoedo_tarta,
					'total_amoedo_integral': total_amoedo_integral,
				}})
			if report_has_refrigerados is True:
				dict_so['categories'].append({'refrigerados': {
					'date_order': date_order,
					'name': name,
					'casa_vegana': casa_vegana,
					'casa_vegana_toq': casa_vegana_toq,
					'vivet_leche': vivet_leche,
					'vivet_queso': vivet_queso,
					'sirius': sirius,
					'placer': placer,
					'quimya': quimya,
					'fv_cheddar': fv_cheddar,
					'fv_provoleta': fv_provoleta,
					'fv_mozza': fv_mozza,
					'fv_hummus': fv_hummus,
					'fv_yogurt': fv_yogurt,
					'fv_dulce_ch': fv_dulce_ch,
					'fv_dulce_gr': fv_dulce_gr,
					'fv_alfajor': fv_alfajor,
					'logo': logo,
					'cudda_hormita': cudda_hormita,
					'cudda_untable': cudda_untable,
					'nina_refr': nina_refr,
					'quimya_yog': quimya_yog,
					'augus_untable': augus_untable,
					'augus_horma': augus_horma,
					'kombucha_refr': kombucha_refr,
					'fv_botell_ch': fv_botell_ch,
					'fv_crema': fv_crema,
					'jugo_litro': jugo_litro,
					'cacah_vivet': cacah_vivet,
					'notco': notco,
					'silk_refr': silk_refr,
					'dale_coco_refr': dale_coco_refr,
					'sonder': sonder,
					'total_casa_vegana': total_casa_vegana,
					'total_casa_vegana_toq': total_casa_vegana_toq,
					'total_vivet_leche': total_vivet_leche,
					'total_vivet_queso': total_vivet_queso,
					'total_sirius': total_sirius,
					'total_placer': total_placer,
					'total_quimya': total_quimya,
					'total_fv_cheddar': total_fv_cheddar,
					'total_fv_provoleta': total_fv_provoleta,
					'total_fv_mozza': total_fv_mozza,
					'total_fv_hummus': total_fv_hummus,
					'total_fv_yogurt': total_fv_yogurt,
					'total_fv_dulce_ch': total_fv_dulce_ch,
					'total_fv_dulce_gr': total_fv_dulce_gr,
					'total_fv_alfajor': total_fv_alfajor,
					'total_logo': total_logo,
					'total_cudda_hormita': total_cudda_hormita,
					'total_cudda_untable': total_cudda_untable,
					'total_nina_refr': total_nina_refr,
					'total_quimya_yog': total_quimya_yog,
					'total_augus_untable': total_augus_untable,
					'total_augus_horma': total_augus_horma,
					'total_kombucha_refr': total_kombucha_refr,
					'total_fv_botell_ch': total_fv_botell_ch,
					'total_fv_crema': total_fv_crema ,
					'total_jugo_litro': total_jugo_litro,
					'total_cacah_vivet': total_cacah_vivet,
					'total_notco': total_notco,
					'total_silk_refr': total_silk_refr,
					'total_dale_coco_refr': total_dale_coco_refr,
					'total_sonder': total_sonder,
				}})
			if report_has_secos is True:
				dict_so['categories'].append({'secos': {
					'date_order': date_order,
					'name': name,
					'vivet_cacahuate': vivet_cacahuate,
					'quimya_granola': quimya_granola,
					'kombucha': kombucha,
					'felices_alfajor': felices_alfajor,
					'nina_sec': nina_sec,
					'pf_litro': pf_litro,
					'pf_500ml': pf_500ml,
					'pf_330ml': pf_330ml,
					'pf_200ml': pf_200ml,
					'notmayo': notmayo,
					'notmilk': notmilk,
					'silk': silk,
					'dale_coco': dale_coco,
					'total_vivet_cacahuate': total_vivet_cacahuate,
					'total_quimya_granola': total_quimya_granola,
					'total_kombucha': total_kombucha,
					'total_felices_alfajor': total_felices_alfajor,
					'total_nina_sec': total_nina_sec,
					'total_pf_litro': total_pf_litro,
					'total_pf_500ml': total_pf_500ml,
					'total_pf_330ml': total_pf_330ml,
					'total_pf_200ml': total_pf_200ml,
					'total_notmayo': total_notmayo,
					'total_notmilk': total_notmilk,
					'total_silk': total_silk,
					'total_dale_coco': total_dale_coco,
				}})

			list_so.append(dict_so)

		if len(list_so) == 1:
			street = so.partner_id.street if so.partner_id.street is not False else ''
			city = so.partner_id.city if so.partner_id.city is not False else ''
			for rec in list_so:
				rec['resumen'] = {
					'cliente': so.partner_id.name,
					'dir': '%s %s' %(street, city),
					'subtotal': so.amount_untaxed,
					'total': so.amount_total,
					'deuda': so.get_deuda_total(so.partner_id),
					'url': 'https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl=%s' %(so.name)
				}
			
		# _logger.info(list_so)
		docargs = {
			'doc_ids': docids,
			'doc_model': report.model,
			'docs': list_so,
		}

		return docargs
	
	def _init_dict_items_congelados(self):
		"""
			Inicializa los diccionarios de 
			los items por categoría ecommerce
			congelados
		"""
		dict_burganas = {
			'berenjena': 0,
			'brocoli': 0,
			'calabaza': 0,
			'cebolla': 0,
			'espinaca': 0,
			'lentejas': 0,
			'tomate': 0,
			'romero': 0,
		}

		dict_cajas_burganas = {
			'caja_berenjena': 0,
			'galletitas': 0,
			'caja_calabaza': 0,
			'caja_cebolla': 0,
			'caja_espinaca': 0,
			'caja_lentejas': 0,
			'caja_tomate': 0,
			'caja_zanahoria': 0,
			'caja_surtida': 0,
			}

		dict_frutas_gr = {
			'arandano_600g': 0,
			'frambuesa_450g': 0,
			'frutilla_600g': 0,
			'mix_berries_600g': 0,
		}

		dict_frutas_ch = {
			'frutilla_durazno_300g': 0,
			'mix_3_berries_300g': 0,
			'mango_maracuya_300g': 0,
		}

		dict_rebozados_kari = {
			'champi': 0,
			'brocoli': 0,
			'aros': 0,
		}

		dict_bites = {
			'bites_arandanos': 0,
			'bites_frambuesas': 0,
			'calabaza': 0,
			'bites_frutilla': 0,
		}

		dict_tortas = {
			'blanco_y_frambuesa': 0,
			'black_forest': 0,
			'marquise': 0,
			'nut_pie': 0,
		}

		dict_haulani_180 = {
			'coco': 0,
		}
		
		dict_haulani_500 = {
			'frutilla': 0,
			'dulce_de_leche': 0,
			'chocolate': 0,
			'mantequilla': 0,
			'blanco': 0,
			'matcha': 0,
		}

		dict_kaira_cla_250 = {
			'dulce_de_leche': 0,
			'chocolate': 0,
		}

		dict_kaira_liv_500 = {
			'chocolate': 0,
			'banana_split': 0,	
		}

		dict_kaira_liv_250 = {
			'chocolate': 0,
		}

		dict_kaira_liv_120 = {
			'chocolate': 0,
			'banana_split': 0,
		}

		dict_ravioles = {
			'calabaza': 0,
			'espinaca': 0,
			'champi': 0,
			'4_quesos': 0,
			'muzza': 0,
		}

		dict_postre = {
			'am_c_dulce_de_leche': 0,
			'am_c_arandanos': 0,
			'choco_c_dulce_de_leche': 0,
		}

		dict_samosas_ch = {
			'papa': 0,
			'calabaza': 0,
			'batata': 0,
			'caprese': 0,
		}

		dict_pizza = {
			'calabaza': 0,
			'brocoli': 0,
		}

		dict_pizza_veg = {
			'zanahoria': 0,
			'calabaza': 0,
			'brocoli': 0,
		}

		dict_croqueta = {
			'espinaca': 0,
			'calabaza': 0,
			'batata': 0,
			'papa': 0,
			'espi_veg': 0,
			'calabaza_veg': 0,
		}

		dict_station = {
			'bocadito': 0,
			'caprese': 0,
		}

		dict_kari_yogt_ch = {
			'choconut': 0,
			'choco_amargo': 0,
			'dulce_de_leche': 0,
			'frutilla': 0,
			'frutos_del_bosque': 0,
			'maracuya': 0,
			'griego': 0,
		}

		dict_kari_yogt_gr = {
			'frutos_del_bosque': 0,
			'maracuya': 0,
		}

		dict_amoedo_tarta = {
			'cala': 0,
			'cebo': 0,
			'caprese': 0,
		}

		dict_amoedo_integral = {
			'cala': 0,
			'zana': 0,
		}

		return dict_burganas, \
			dict_cajas_burganas, \
			dict_frutas_gr, \
			dict_frutas_ch, \
			dict_rebozados_kari, \
			dict_bites, \
			dict_tortas, \
			dict_haulani_180, \
			dict_haulani_500, \
			dict_kaira_cla_250, \
			dict_kaira_liv_500, \
			dict_kaira_liv_250, \
			dict_kaira_liv_120, \
			dict_ravioles, \
			dict_postre, \
			dict_samosas_ch, \
			dict_pizza, \
			dict_pizza_veg, \
			dict_croqueta, \
			dict_station, \
			dict_kari_yogt_ch, \
			dict_kari_yogt_gr, \
			dict_amoedo_tarta, \
			dict_amoedo_integral

	def _init_dict_items_refrigerados(self):
		"""
			Inicializa los diccionarios de 
			los items por categoría ecommerce
			refreigerados
		"""

		dict_casa_vegana = {
			'quinoa_andina': 0,
			'quinoa_hindu': 0,
			'quinoa_sin_sal': 0,
			'quinoa_mediterranea': 0,
			'mijo': 0,
			'yamani': 0,
			'lentejon': 0,
			'aduki_remolacha': 0,
			'aduki_hungaro': 0,
			'green_moon': 0,
		}

		dict_casa_vegana_toq = {
			'falafel': 0,
			'nugget': 0,
		}

		dict_vivet_leche = {
			'original': 0,
			'vainilla': 0,
			'frutilla': 0,
			'chocolate': 0,
			'cafe_latte': 0,
		}

		dict_vivet_queso = {
			'natural': 0,
			'fina_hierbas': 0,
		}

		dict_sirius = {
			'sirius': 0,
		}

		dict_placer = {
			'vainilla': 0,
		}

		dict_quimya = {
			'frutilla': 0,
			'mango': 0,
			'vainilla': 0,
			'arandanos': 0,
			'chocolate': 0,
			'coconut': 0,
			'keylime_palta_granola': 0,
			'natural_con_granola': 0,
		}

		dict_fv_cheddar = {
			'cheddar': 0,
		}

		dict_fv_provoleta = {
			'provoleta': 0,
		}

		dict_fv_mozza = {
			'mozarella': 0,
		}

		dict_fv_hummus = {
			'hummus': 0,
		}

		dict_fv_yogurt = {
			'yogurt_frutilla': 0,
			'yogurt_durazno': 0,
			'yogurt_cereales': 0,
		}

		dict_fv_dulce_ch = {
			'dulce_ch': 0,
		}

		dict_fv_dulce_gr = {
			'dulce_gr': 0,
		}

		dict_fv_alfajor = {
			'alfajor_maicena': 0,
			'alfajor_chocolate': 0,
		}

		dict_logo = {
			'logo_natural': 0,
			'logo_frutilla': 0,
			'logo_vainilla': 0,
			'logo_arandanos': 0,
			'logo_maracuya': 0,
			'logo_durazno_s_azucar': 0,
			'logo_frutilla_s_azucar': 0,
			'logo_natural_granola': 0,
			'logo_vainilla_granola': 0,
		}

		dict_cudda_hormita = {
			'crudda_clasico': 0,
			'crudda_provence': 0,
			'crudda_ahumado': 0,
			'crudda_pimienta': 0,
		}

		dict_cudda_untable = {
			'crudda_untable':0,
		}

		dict_nina = {
			'chocolate':0,
			'blondies':0,
			'cranberry':0,
			'chocochips':0,
			'biscochitos': 0,
			'sugar_limon': 0,
		}

		dict_quimya_yog = {
			'untable_felicia': 0,
		}

		dict_augus_untable = {
			'clasico': 0,
			'ciboulette': 0,
			'pimenton': 0,
		}

		dict_augus_horma = {
			'clasica': 0,
			'hierbas': 0,
			'camembert': 0,
		}

		dict_kombucha = {
			'verde': 0,
		}

		dict_fv_botell_ch = {
			'leche_almendra': 0,
			'leche_chocolatada': 0,
			'leche_coco': 0,
			'smoothie_frutos': 0,
			'smoothie_mango': 0,
			'smoothie_banana': 0,
		}

		dict_fv_crema = {
			'crema': 0,
		}

		dict_jugo_litro = {
			'rojo': 0,
		}

		dict_cacah_vivet = {
			'vainilla': 0,
			'choco': 0,
		}

		dict_notco = {
			'mayo': 0,
			'notmilk': 0,
		}

		dict_silk = {
			'almendra': 0,
			's_azucar': 0,
			'coco': 0,
		}

		dict_dale_coco = {
			'leche_de_coco': 0,
		}

		dict_sonder = {
			'green_tree': 0,
			'sunrise': 0,
		}

		return dict_casa_vegana, \
			dict_casa_vegana_toq, \
			dict_vivet_leche, \
			dict_vivet_queso, \
			dict_sirius, \
			dict_placer, \
			dict_quimya, \
			dict_fv_cheddar, \
			dict_fv_provoleta, \
			dict_fv_mozza, \
			dict_fv_hummus, \
			dict_fv_yogurt, \
			dict_fv_dulce_ch, \
			dict_fv_dulce_gr, \
			dict_fv_alfajor, \
			dict_logo, \
			dict_cudda_hormita, \
			dict_cudda_untable, \
			dict_nina, \
			dict_quimya_yog, \
			dict_augus_untable, \
			dict_augus_horma, \
			dict_kombucha, \
			dict_fv_botell_ch, \
			dict_fv_crema, \
			dict_jugo_litro, \
			dict_cacah_vivet, \
			dict_notco, \
			dict_silk, \
			dict_dale_coco, \
			dict_sonder

	def _init_dict_items_secos(self):
		"""
			Inicializa los diccionarios de 
			los items por categoría ecommerce
			secos
		"""

		dict_vivet_cacahuate = {
			'cacao': 0,
			'vainilla_natural': 0,
			'vainilla_caramel': 0,
		}

		dict_quimya_granola = {
			'familiar': 0,
			'individual': 0,
		}

		dict_kombucha = {
			'negro': 0,
			'rojo': 0,
			'verde': 0,
		}

		dict_felices_alfajor = {
			'chocolate': 0,
			'maicena': 0,
		}

		dict_nina = {
			'bizcochitos': 0,
			'blondie': 0,
			'choco': 0,
			'chocochips': 0,
			'cranberry': 0,
			'limon': 0,
			'limon_sugar_free': 0,
			'blondies_sugar_free': 0,
		}

		dict_pf_litro = {
			'manzana_roja': 0,
			'manzana_verde': 0,
			'organico': 0,
			'naranja': 0,
			'arandanos': 0,
			'frutilla': 0,
			'kiwi': 0,
		}

		dict_pf_500ml = {
			'manzana_roja': 0,
			'manzana_verde': 0,
		}

		dict_pf_330ml = {
			'naranja': 0,
		}

		dict_pf_200ml = {
			'manzana_roja': 0,
			'manzana_verde': 0,
		}

		dict_notmayo = {
			'mayonesa': 0
		}

		dict_notmilk = {
			'not_milk': 0,
			'promocion': 0,
		}

		dict_silk = {
			'alm_vainilla': 0,
			'almendra': 0,
			'almendra_sin_azucar': 0,
			'chocolatada': 0,
			'coco': 0,
		}

		dict_dale_coco = {
			'agua_de_coco': 0,
			'leche_de_coco': 0,
		}

		return dict_vivet_cacahuate, dict_quimya_granola, dict_kombucha, dict_felices_alfajor, dict_nina, dict_pf_litro, dict_pf_500ml, dict_pf_330ml, dict_pf_200ml, dict_notmayo, dict_notmilk, dict_silk, dict_dale_coco
