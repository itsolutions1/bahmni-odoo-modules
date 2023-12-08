# -*- coding: utf-8 -*-
from odoo import models, fields, api
from decouple import config
import psycopg2
import threading
import time


class jss_data_import(models.Model):
     _name = 'jss_data_import'
     _description = 'JSS Data Import'

     def connect_to_external_db(self):
        """ To connect the external database """
        try:
            conn = psycopg2.connect(
                dbname= config('JSS_DB_NAME'),
                user= config('JSS_DB_USER'),
                password= config('JSS_DB_PASSWORD'),
                host= config('JSS_DB_HOST'),
                port= config('JSS_DB_PORT')
            )
            return conn
        except Exception as e:
            raise e

     def execute_query(self, conn, sql_query):
        """ Query execution block """
        try:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            raise e


     def close_connection(self, conn):
        """ Connection closing block """
        try:
            if conn:
                conn.close()
        except Exception as e:
            raise e

     def customer_data_feed(self, start_id, end_id):
         """ Customer data from the openerp 7 """

         external_conn = self.connect_to_external_db()
         if external_conn:
             try:
                 query = """ select name,lang,company_id,create_uid,create_date,write_date,write_uid,color,
                        image,use_parent_address,active,street,supplier,city,user_id,zip,title,function,country_id,
                        parent_id,employee,type,email,vat,website,fax,street2,phone,credit_limit,date,tz,customer,
                        mobile,ref,is_company,state_id,notification_email_send,
                        signup_type,signup_expiration,signup_token,last_reconciliation_date,debit_limit,village,
                        local_name,uuid from res_partner where customer= 't' and id > %s and id < %s """ %(start_id, end_id)
                 result = self.execute_query(external_conn, query)
                 partner_to = self.env['res.partner']
                 count = 1
                 if result:
                    for partner_from in result:
                         if partner_to.search([("uuid", '=', partner_from[44] if partner_from[44] else False),"|", ('active', '=', True)\
                                                ,('active', '=', False)]):
                            print("PASS")
                            pass
                         else:
                            print("partner_from:", partner_from)                            
                            print("++++++++++++++++++++++count:", count)                            
                            def _greb_village(v_name):
                                """ Village fetching & creation """
                                if v_name:
                                    village_rec = self.env['village.village']
                                    identified_villages = village_rec.search([('name', '=', v_name)], limit=1)
                                    if identified_villages:
                                        return identified_villages.id
                                    else:
                                        return village_rec.create({'name': v_name}).id
                            count += 1
                            partner_to.create({
                                            "name"      : partner_from[0] if partner_from[0] else False,
                                            "display_name"      : partner_from[0] if partner_from[0] else False,
                                            "lang"    : partner_from[1] if partner_from[1] else False,
                                            "company_id"   : partner_from[2] if partner_from[2] else False,
                                            "create_uid"      : partner_from[3] if partner_from[3] else False,
                                            "create_date"       : partner_from[4] if partner_from[4] else False,
                                            "write_date"      : partner_from[5] if partner_from[5] else False,
                                            "write_uid"     : partner_from[6] if partner_from[6] else False,
                                            "color"     : partner_from[7] if partner_from[7] else False,
                                            "use_parent_address"    : partner_from[9] if partner_from[9] else False,
                                            "active": partner_from[10] if partner_from[10] else False,
                                            "street": partner_from[11] if partner_from[11] else False,
                                            "supplier_rank": 0,
                                            "customer_rank": 1,
                                            "city": partner_from[13] if partner_from[13] else False,  
                                            "user_id": partner_from[14] if partner_from[14] else False,  
                                            "zip": partner_from[15] if partner_from[15] else False,  
                                            "title": partner_from[16] if partner_from[16] else False,  
                                            "function": partner_from[17] if partner_from[17] else False,  
                                            "country_id": partner_from[18] if partner_from[18] else False,  
                                            "parent_id": partner_from[19] if partner_from[19] else False,  
                                            "employee": partner_from[20] if partner_from[20] else False,  
                                            "email": partner_from[22] if partner_from[22] else False,  
                                            "vat": partner_from[23] if partner_from[23] else False,  
                                            "website": partner_from[24] if partner_from[24] else False,  
                                            "street2": partner_from[26] if partner_from[26] else False,  
                                            "phone": partner_from[27] if partner_from[27] else False,  
                                            "credit_limit": partner_from[28] if partner_from[28] else False,  
                                            "date": partner_from[29] if partner_from[29] else False,  
                                            "tz": partner_from[30] if partner_from[30] else False,  
                                            "mobile": partner_from[32] if partner_from[32] else False,                                             
                                            "ref": partner_from[33] if partner_from[33] else False,  
                                            "is_company": partner_from[34] if partner_from[34] else False,  
                                            "state_id": partner_from[35] if partner_from[35] else False,  
                                            "notification_email_send": partner_from[36] if partner_from[36] else False,  
                                            "signup_type": partner_from[37] if partner_from[37] else False,  
                                            "signup_expiration": partner_from[38] if partner_from[38] else False,  
                                            "signup_token": partner_from[39] if partner_from[39] else False,  
                                            "last_reconciliation_date": partner_from[40] if partner_from[40] else False,  
                                            "debit_limit": partner_from[41] if partner_from[41] else False,  
                                            "village_id": _greb_village(partner_from[42] if partner_from[42] else False),  
                                            "local_name": partner_from[43] if partner_from[43] else False,  
                                            "uuid": partner_from[44] if partner_from[44] else False,  

                                    })
             finally:
               self.close_connection(external_conn)
         return True

     def supplier_data_feed(self, start_id, end_id):
         """ supplier data from the openerp 7 """

         external_conn = self.connect_to_external_db()
         if external_conn:
             try:
                 query = """ select name,lang,company_id,create_uid,create_date,write_date,write_uid,color,
                        image,use_parent_address,active,street,supplier,city,user_id,zip,title,function,country_id,
                        parent_id,employee,type,email,vat,website,fax,street2,phone,credit_limit,date,tz,customer,
                        mobile,ref,is_company,state_id,notification_email_send,
                        signup_type,signup_expiration,signup_token,last_reconciliation_date,debit_limit,village,
                        local_name,uuid from res_partner where supplier= 't' and id > %s and id < %s """ %(start_id, end_id)
                 result = self.execute_query(external_conn, query)
                 partner_to = self.env['res.partner']
                 count = 1
                 if result:
                    for partner_from in result:
                         if partner_to.search([("name", '=', partner_from[0] if partner_from[0] else False),"|", ('active', '=', True)\
                                                ,('active', '=', False)]):
                            print("PASS")
                            pass
                         else:
                            print("partner_from:", partner_from)                            
                            print("++++++++++++++++++++++count:", count)                            
                            def _greb_village(v_name):
                                """ Village fetching & creation """
                                if v_name:
                                    village_rec = self.env['village.village']
                                    identified_villages = village_rec.search([('name', '=', v_name)], limit=1)
                                    if identified_villages:
                                        return identified_villages.id
                                    else:
                                        return village_rec.create({'name': v_name}).id
                            count += 1
                            partner_to.create({
                                            "name"      : partner_from[0] if partner_from[0] else False,
                                            "display_name"      : partner_from[0] if partner_from[0] else False,
                                            "lang"    : partner_from[1] if partner_from[1] else False,
                                            "company_id"   : partner_from[2] if partner_from[2] else False,
                                            "create_uid"      : partner_from[3] if partner_from[3] else False,
                                            "create_date"       : partner_from[4] if partner_from[4] else False,
                                            "write_date"      : partner_from[5] if partner_from[5] else False,
                                            "write_uid"     : partner_from[6] if partner_from[6] else False,
                                            "color"     : partner_from[7] if partner_from[7] else False,
                                            "use_parent_address"    : partner_from[9] if partner_from[9] else False,
                                            "active": partner_from[10] if partner_from[10] else False,
                                            "street": partner_from[11] if partner_from[11] else False,
                                            "supplier_rank": 1,
                                            "customer_rank": 0, 
                                            "city": partner_from[13] if partner_from[13] else False,  
                                            "user_id": partner_from[14] if partner_from[14] else False,  
                                            "zip": partner_from[15] if partner_from[15] else False,  
                                            "title": partner_from[16] if partner_from[16] else False,  
                                            "function": partner_from[17] if partner_from[17] else False,  
                                            "country_id": partner_from[18] if partner_from[18] else False,  
                                            "parent_id": partner_from[19] if partner_from[19] else False,  
                                            "employee": partner_from[20] if partner_from[20] else False,  
                                            "email": partner_from[22] if partner_from[22] else False,  
                                            "vat": partner_from[23] if partner_from[23] else False,  
                                            "website": partner_from[24] if partner_from[24] else False,  
                                            "street2": partner_from[26] if partner_from[26] else False,  
                                            "phone": partner_from[27] if partner_from[27] else False,  
                                            "credit_limit": partner_from[28] if partner_from[28] else False,  
                                            "date": partner_from[29] if partner_from[29] else False,  
                                            "tz": partner_from[30] if partner_from[30] else False,  
                                            "mobile": partner_from[32] if partner_from[32] else False,                                             
                                            "ref": partner_from[33] if partner_from[33] else False,  
                                            "is_company": partner_from[34] if partner_from[34] else False,  
                                            "state_id": partner_from[35] if partner_from[35] else False,  
                                            "notification_email_send": partner_from[36] if partner_from[36] else False,  
                                            "signup_type": partner_from[37] if partner_from[37] else False,  
                                            "signup_expiration": partner_from[38] if partner_from[38] else False,  
                                            "signup_token": partner_from[39] if partner_from[39] else False,  
                                            "last_reconciliation_date": partner_from[40] if partner_from[40] else False,  
                                            "debit_limit": partner_from[41] if partner_from[41] else False,  
                                            "village_id": _greb_village(partner_from[42] if partner_from[42] else False),  
                                            "local_name": partner_from[43] if partner_from[43] else False,  
                                            "uuid": partner_from[44] if partner_from[44] else False,  

                                    })
             finally:
               self.close_connection(external_conn)

     def uom_category_data_feed(self):
         """ UOM category from the openerp 7 """
         external_conn = self.connect_to_external_db()
         if external_conn:
             try:
                query = """ select name,uuid from product_uom_categ """
                result = self.execute_query(external_conn, query)
                uom_cate_to = self.env['uom.category']
                if result:
                    for uom_cate_from in result:
                        available_uom = uom_cate_to.search([("name", '=', uom_cate_from[0] if uom_cate_from[0] else False)])
                        if available_uom:
                            if not available_uom.uuid:
                                available_uom.uuid = uom_cate_from[1] if uom_cate_from[1] else False
                            pass
                        else:
                            uom_cate_mapping = uom_cate_to.create({
                                                "name": uom_cate_from[0] if uom_cate_from[0] else False,
                                                "uuid": uom_cate_from[1] if uom_cate_from[1] else False})
             finally:
                self.close_connection(external_conn)


     def uom_data_feed(self):
         """ uom data from the openerp 7 """
         external_conn = self.connect_to_external_db()
         if external_conn:
             try:
                query = """select uom.uuid,uom.name,uom.uom_type,uom.rounding,uom.factor,uom.active,cat.name,uom.id from 
                 product_uom uom
                 left join product_uom_categ cat on (cat.id =  uom.category_id) order by uom.id desc"""
                result = self.execute_query(external_conn, query)
                print("results", result)
                uom_to = self.env['uom.uom']
                if result:
                    for uom_from in result:
                        if uom_to.search([("uuid", '=', uom_from[0] if uom_from[0] else False),"|", ('active', '=', True)\
                                                ,('active', '=', False)]):
                            pass
                        else:
                            uom_mapping = uom_to.create({
                                                "uuid": uom_from[0] if uom_from[0] else False,
                                                "name": uom_from[1] if uom_from[1] else False, 
                                                "uom_type": 'bigger', 
                                                "rounding": uom_from[3] if uom_from[3] else False,
                                                "factor": uom_from[4] if uom_from[4] else False,
                                                "active": uom_from[5] if uom_from[5] else False,
                                                "category_id": self.env['uom.category'].search([\
                                                    ('name', '=', uom_from[6] if uom_from[6] else False)], limit=1).id})
             finally:
                self.close_connection(external_conn)

     def product_category_data_feed(self):
         """ Product Category data from the openerp 7 """

         external_conn = self.connect_to_external_db()
         if external_conn:
             try:
                query = "SELECT name,uuid from product_category order by id desc"
                result = self.execute_query(external_conn, query)
                product_cate_to = self.env['product.category']
                if result:
                    for product_cate_from in result:
                        if product_cate_to.search([("uuid", '=', product_cate_from[1] if product_cate_from[1] else False)]):
                            pass
                        else:
                            if product_cate_from[0]: ##without name with uuid data not allowed. 
                                product_cate_mapping = product_cate_to.create({
                                                    "name": product_cate_from[0] if product_cate_from[0] else False,
                                                    "uuid": product_cate_from[1] if product_cate_from[1] else False})
             finally:
                self.close_connection(external_conn)

     def product_data_feed(self):
         """ Product data from the openerp 7 """
         external_conn = self.connect_to_external_db()
         if external_conn:
             try:
                query = """ select pt.name,pt.type,pp.uuid,
                    pp.active,pp.manufacturer,
                    pp.drug,pp.use_time,pp.life_time,pp.removal_time,pp.alert_time,
                    pt.list_price,pt.description,pt.weight,pt.weight_net,
                    pu.name,pt.description_purchase,pt.cost_method,pc.name,pt.volume,pt.sale_ok,pt.description_sale,
                    pu1.name,pt.sale_delay,pt.purchase_ok,pp.id
                    from product_product pp left join product_template pt on pt.id = pp.product_tmpl_id 
                    left join product_category pc on pt.categ_id = pc.id 
                    left join product_uom pu on pt.uom_id = pu.id 
                    left join product_uom pu1 on pt.uom_po_id = pu1.id where pp.id not in (3048,2076,2073) order by pp.id desc"""
                result = self.execute_query(external_conn, query)
                product_to = self.env['product.product']
                if result:
                    for product_from in result:
                        if product_to.search([("uuid", '=', product_from[2] if product_from[2] else False),"|", ('active', '=', True)\
                                                ,('active', '=', False)]):
                            pass
                        else:
                            print("product_from[24]",product_from[24])
                            print("product_from[0] if product_from[0] else False",product_from[0] if product_from[0] else False)
                            print("product_from[21]",product_from[21])
                            print("self.env['uom.uom'].search([('name', '=', product_from[21])], limit=1).id[21]",self.env['uom.uom'].search([('name', '=', product_from[21])], limit=1).id)
                            print("self.env['uom.uom'].search([('name', '=', product_from[14])], limit=1).id",self.env['uom.uom'].search([('name', '=', product_from[14])], limit=1).id)
                            print("product_from[14]",product_from[14])
                            product_mapping = product_to.create({
                                                "name": product_from[0] if product_from[0] else False,
                                                "type": product_from[1] if product_from[1] else False,
                                                "uuid": product_from[2] if product_from[2] else False,
                                                "active": product_from[3] if product_from[3] else False,
                                                #"manufacturer": product_from[4] if product_from[4] else False, ## Char in v7 int in v16
                                                "drug": product_from[5] if product_from[5] else False,
                                                "use_time": product_from[6] if product_from[6] else False,
                                                "expiration_time": product_from[7] if product_from[7] else False,
                                                "removal_time": product_from[8] if product_from[8] else False,
                                                "alert_time": product_from[9] if product_from[9] else False,
                                                "list_price": product_from[10] if product_from[10] else False,
                                                "description": product_from[11] if product_from[11] else False,
                                                "weight": product_from[12] if product_from[12] else False,
                                                "to_weight": product_from[13] if product_from[13] else False,
                                                "uom_id": self.env['uom.uom'].search([('name', '=', product_from[14])], limit=1).id,
                                                "description_purchase": product_from[15] if product_from[15] else False,
                                                "categ_id": self.env['product.category'].search([('name', '=', product_from[17])],limit=1).id if self.env['product.category'].search([('name', '=', product_from[17])],limit=1).id else 1,
                                                "volume": product_from[18] if product_from[18] else False,
                                                "sale_ok": product_from[19] if product_from[19] else False,
                                                "description_sale": product_from[20] if product_from[20] else False,
                                                "uom_po_id": self.env['uom.uom'].search([('name', '=', product_from[21])], limit=1).id,
                                                "sale_delay": product_from[22] if product_from[22] else False,
                                                "purchase_ok": product_from[23] if product_from[23] else False})
             finally:
                self.close_connection(external_conn)
