#!/usr/bin/python
import shopify
from config_stuff import *
import sqlite3
import time
import datetime
from pprint import pprint

class ShopifyInterface():
    def __init__(self):
        #self.db = sqlite3.connect(DB_FILE)
        #self.db_cursor = self.db.cursor()
        
        f = open(SHOPIFY_PLAID_ROOM_NAME, 'r')
        #f = open(SHOPIFY_COLEMINE_NAME, 'r')
        
        self.api_key = (f.readline()).strip()
        self.api_password = (f.readline()).strip()
        
        shop_url = "https://%s:%s@plaid-room-records-2.myshopify.com/admin" % (self.api_key, self.api_password)
        #shop_url = "
        shopify.ShopifyResource.set_site(shop_url)
        #shop_url = "https://%s:%s@colemine-records.myshopify.com/admin" % (self.api_key, self.api_password)
        #shopify.ShopifyResource.set_site(shop_url)

    def get_trans_info(self, shopify_id):
        order = shopify.Order.find(shopify_id)
        return order
        
        
    def get_line_items(self, shopify_id):
        order = shopify.Order.find(shopify_id)
        print order
        #print order.attributes
        items_to_return = []
        for line in order.line_items:
#            to_append = [line["sku"],line["price"],line["variant_title"]]
            to_append = [line.sku,line.price,line.title,line.quantity]
            items_to_return.append(to_append)
        return items_to_return
        
    def get_list_of_orders_after_order_number(self, shopify_id):
        orders_to_return = []
        for page in range(250):
            orders = shopify.Order.find(page=(page+1), since_id=shopify_id)
            time.sleep(0.5)
            if len(orders) == 0:
                break
            for order in orders:
                qty = 0
                #print order
                for line in order.line_items:
                    qty += int(line.quantity)
                #print '%s - %s items' % (order.name,str(qty))
                print order
                print order.shipping_lines
                ship_temp = ''
                if len(order.shipping_lines) == 0:
                    ship_temp = 'ERROR'
                else:
                    ship_temp = order.shipping_lines[0].attributes["title"]
                to_append = [order.id, order.processed_at, qty, order.total_price, ship_temp, 0]
                orders_to_return.append(to_append)
                #print order.attributes
                #print order
                #print '\n\n\n'
        #print 'total orders: %s' % (str(total),)
        return orders_to_return

            
    def get_list_of_orders_from_beginning(self):
        #order_number = range(520)
        orders_to_return = []
        for page in range(250):
            #print '\n\n -------------\t\tPAGE %s\t\t--------------------\n\n' % (str(page+1),)
            orders = shopify.Order.find(page=(page+1))#status will default to status='open', use status='any' to get ALL orders, including refunds
            time.sleep(0.5)
            if len(orders) == 0:
                break
            for order in orders:
                try:
                    order_id = 0
                    order_id = order.id
                    qty = 0
                    #print order
                    for line in order.line_items:
                        qty += int(line.quantity)
                    #print '%s - %s items' % (order.name,str(qty))
                    to_append = [order.id, order.processed_at, qty, order.total_price, order.shipping_lines[0].attributes["title"],0]
                    orders_to_return.append(to_append)
                    #print order.attributes
                    #print order
                    #print '\n\n\n'
                except Exception as e:
                    print 'trouble getting order: %s' % (order_id)
        #print 'total orders: %s' % (str(total),)
        return orders_to_return
        
    def delete_item(self, id):
        product = shopify.Product.find(id)
        time.sleep(0.5)
        try:
            product.destroy()
            return True
        except Exception as e:
            return False

    def get_item(self, id):
        product = shopify.Product.find(id)
        time.sleep(0.5)
        return product

    def update_pictures_for_upc(self, row):
        print 'about to call Image()'
        image = shopify.Image()
        print 'called Image()'
        image.position = int(row[IMAGE_POSITION])
        print 'image position: %s' % str(row[IMAGE_POSITION])
        file_name = '%s%s' % (WEBSITE_IMAGES,row[IMAGE_FILENAME])
        print file_name
        f = open(file_name, "rb")
        image.attach_image(f.read())
        image.product_id = row[IMAGE_SHOPIFY_PRODUCT]
        product = shopify.Product.find(row[IMAGE_SHOPIFY_PRODUCT])
        time.sleep(0.25)
        product.images.append(image)
        #product.images = [image]
        try:
            success = product.save()
            time.sleep(0.5)
            if success:
                return product
        except Exception as e:
            print 'problem tryna upload pics to shopify: %s' % e
            return None
        return None
            

    def create_or_update_catalog_item(self, row):#aka sync
        placeholder = 0
        if row[ONLINE_SHOPIFY_ID] is None or row[ONLINE_SHOPIFY_ID] == '':#if it doesn't exist
            try:
                new_product = shopify.Product()
                #street_date_formatted_for_america = datetime.datetime.strptime(row[PRE_STREET_DATE], "%Y-%m-%d")
                #street_date_formatted_for_america = street_date_formatted_for_america.strftime("%m/%d/%Y")
                new_product.title = "<b>%s </b><br><i>%s</i>" % (row[ONLINE_ARTIST], row[ONLINE_TITLE])
                if 'BF2017' in row[ONLINE_SHOPIFY_TAGS]:
                    new_product.product_type = "BF2017"#default for now, might change later
                else:
                    new_product.product_type = "LP"#default for now, might change later
                #build tags
                if len(row[ONLINE_GENRE]) > 1:
                    genres = [x.strip() for x in row[ONLINE_GENRE].split(',')]
                genres_split = []
                for genre in genres:
                    genres_split.append('Genre_%s' % genre)
                genre_tags_to_add = ",".join(genres_split)
                new_product.tags = genre_tags_to_add + ',' + row[ONLINE_SHOPIFY_TAGS]
                #build description
                desc = '<b>UPC: %s </b><br>' % row[ONLINE_UPC]
                if len(row[ONLINE_LABEL]) > 1:
                    desc += 'Label: %s <br>' % row[ONLINE_LABEL]
                desc += 'Format: %s <br>' % row[ONLINE_FORMAT]
                if len(row[ONLINE_STREET_DATE]) > 1:
                    desc += 'Release Date: %s <br>' % row[ONLINE_STREET_DATE]
                desc += 'In stock items ship within 24 hours. <br>'
                desc += '<br>'
                #new_product.body_html = '<b>UPC: %s </b><br>Format: %s <br>Label: In stock items ship within 24 hours.'
                new_product.body_html = desc + row[ONLINE_SHOPIFY_DESC]
                new_product.metafields_global_title_tag = "%s - %s" % (row[ONLINE_ARTIST], row[ONLINE_TITLE])
                new_product.metafields_global_description_tag = "Order now from an independently owned record store in Cincinnati, OH %s" % (row[ONLINE_UPC])
                pprint (vars(new_product))
                if row[ONLINE_ACTIVE] == 0:
                    new_product.published_at = None
#                else:
#                    product.published_at = datetime.datetime.now().isoformat()
                new_product.published_scope = 'web'
                v = shopify.Variant()
                v.price = row[ONLINE_SALE_PRICE]
                v.sku = row[ONLINE_UPC]
                v.inventory_management = 'shopify'
                v.inventory_policy = 'deny'
                if row[ONLINE_UPC] == '889854196219':
                    v.weight = 17
                    v.weight_unit = 'oz'
                elif row[ONLINE_UPC] == '659123080019':
                    v.weight = '34'
                    v.weight_unit = 'oz'
                elif row[ONLINE_UPC] == '081227941000':
                    v.weight = 17
                    v.weight_unit = 'oz'
                else:
                    v.weight = 500
                    v.weight_unit = 'lb'
                v.inventory_quantity = row[ONLINE_QOH]
                v.product_id = new_product.id
                new_product.variants = [v]
                success = new_product.save()
                time.sleep(0.25)
                pprint (vars(new_product))
                print
            except Exception as e:
                print 'error in the shopify:create_or_update_item func: %s' % e
                return None
            if success == False:
                return None
            time.sleep(0.5)
            return new_product
        else:
            try:
                product = shopify.Product.find(row[ONLINE_SHOPIFY_ID])
                product.title = "<b>%s </b><br><i>%s</i>" % (row[PRE_ARTIST], row[PRE_TITLE])
                if 'BF2017' in row[ONLINE_SHOPIFY_TAGS]:
                    product.product_type = "BF2017"#default for now, might change later
                else:
                    product.product_type = "LP"#default for now, might change later
                product.tags = row[ONLINE_SHOPIFY_TAGS]
                product.body_html = row[ONLINE_SHOPIFY_DESC]
                #build tags
                if len(row[ONLINE_GENRE]) > 1:
                    genres = [x.strip() for x in row[ONLINE_GENRE].split(',')]
                genres_split = []
                for genre in genres:
                    genres_split.append('Genre_%s' % genre)
                genre_tags_to_add = ",".join(genres_split)
                product.tags = genre_tags_to_add + ',' + row[ONLINE_SHOPIFY_TAGS]
                #build description
                desc = '<b>UPC: %s </b><br>' % row[ONLINE_UPC]
                if len(row[ONLINE_LABEL]) > 1:
                    desc += 'Label: %s <br>' % row[ONLINE_LABEL]
                desc += 'Format: %s <br>' % row[ONLINE_FORMAT]
                if len(row[ONLINE_STREET_DATE]) > 1:
                    desc += 'Release Date: %s <br>' % row[ONLINE_STREET_DATE]
                desc += 'In stock items ship within 24 hours. <br>'
                desc += '<br>'
                #new_product.body_html = '<b>UPC: %s </b><br>Format: %s <br>Label: In stock items ship within 24 hours.'
                product.body_html = desc + row[ONLINE_SHOPIFY_DESC]
                product.metafields_global_title_tag = "%s - %s" % (row[ONLINE_ARTIST], row[ONLINE_TITLE])
                product.metafields_global_description_tag = "Order now from an independently owned record store in Cincinnati, OH %s" % (row[ONLINE_UPC])
                if row[ONLINE_ACTIVE] == 0:
                    product.published_at = None
                else:
                    product.published_at = datetime.datetime.now().isoformat()
                product.published_scope = 'web'
                #v = shopify.Variant()
                v = product.variants[0]
                v.price = row[ONLINE_SALE_PRICE]
                v.sku = row[ONLINE_UPC]
                v.inventory_management = 'shopify'
                v.inventory_policy = 'deny'
                if row[ONLINE_UPC] == '889854196219':
                    v.weight = 17
                    v.weight_unit = 'oz'
                elif row[ONLINE_UPC] == '659123080019':
                    v.weight = '34'
                    v.weight_unit = 'oz'
                elif row[ONLINE_UPC] == '081227941000':
                    v.weight = 17
                    v.weight_unit = 'oz'
                else:
                    v.weight = 500
                    v.weight_unit = 'lb'
                v.inventory_quantity = row[ONLINE_QOH]
                v.product_id = product.id
                #new_product.variants = [v]
                success = product.save()
                #pprint (vars(new_product))
                #print
            except Exception as e:
                print 'error in the shopify:create_or_update_item func (UPDATE): %s' % e
                return None
            if success == False:
                return None
            time.sleep(0.5)
            return product

            #do stuff

    def update_qoh(self, shopify_id, qoh):
        try:
            product = shopify.Product.find(shopify_id)
            v = product.variants[0]
            v.inventory_quantity = qoh
            v.product_id = product.id
            success = product.save()
        except Exception as e:
            print 'error in updating qoh: %s' % e
            return None
        time.sleep(0.75)
        return product
            
    #this function takes an item formatted from the pre-order table in the DB, and updates or creates it on shopify,
    #and also returns the shopify product when it's done
    def create_or_update_item(self, row):#aka sync
        if row[PRE_SHOPIFY_ID] is None or row[PRE_SHOPIFY_ID] == '':#if it doesn't exist
            try:
                new_product = shopify.Product()
                street_date_formatted_for_america = datetime.datetime.strptime(row[PRE_STREET_DATE], "%Y-%m-%d")
                street_date_formatted_for_america = street_date_formatted_for_america.strftime("%m/%d/%Y")
                new_product.title = "<b>%s </b><br><i>%s </i><br>Release Date : %s" % (row[PRE_ARTIST], row[PRE_TITLE], street_date_formatted_for_america)
                new_product.product_type = "LP"#default for now, might change later
                new_product.tags = row[PRE_SHOPIFY_TAGS]

                #build description
                desc = '<b>UPC: %s </b><br>' % row[PRE_UPC]
                if len(row[PRE_LABEL]) > 1:
                    desc += 'Label: %s <br>' % row[PRE_LABEL]
                desc += 'Format: %s <br>' % row[PRE_FORMAT]
                if len(row[PRE_STREET_DATE]) > 1:
                    desc += 'Release Date: %s <br>' % row[PRE_STREET_DATE]
                desc += '<br>'
                #new_product.body_html = '<b>UPC: %s </b><br>Format: %s <br>Label: In stock items ship within 24 hours.'
                new_product.body_html = desc + row[PRE_SHOPIFY_DESC]
                
                #new_product.body_html = row[PRE_SHOPIFY_DESC]
                #new_product.body_html = '<b>UPC: %s </b><br>%s' % (row[PRE_UPC],row[PRE_SHOPIFY_DESC])
                new_product.metafields_global_title_tag = "Pre-Order %s %s" % (row[PRE_ARTIST], row[PRE_TITLE])
                new_product.metafields_global_description_tag = "Pre-order now from an independently owned record store in Cincinnati, OH %s" % (row[PRE_UPC])
                pprint (vars(new_product))
                if row[PRE_ACTIVE] == 0:
                    new_product.published_at = None
#                else:
#                    product.published_at = datetime.datetime.now().isoformat()
                new_product.published_scope = 'web'
                v = shopify.Variant()
                v.price = row[PRE_SALE_PRICE]
                v.sku = row[PRE_UPC]
                v.weight = 500
                v.weight_unit = 'lb'
                v.product_id = new_product.id
                new_product.variants = [v]
                success = new_product.save()
                time.sleep(0.25)
                pprint (vars(new_product))
                print
            except Exception as e:
                print 'error in the shopify:create_or_update_item func: %s' % e
                return None
            if success == False:
                return None
            time.sleep(0.5)
            return new_product
        else:
            try:
                product = shopify.Product.find(row[PRE_SHOPIFY_ID])
                street_date_formatted_for_america = datetime.datetime.strptime(row[PRE_STREET_DATE], "%Y-%m-%d")
                street_date_formatted_for_america = street_date_formatted_for_america.strftime("%m/%d/%Y")
                product.title = "<b>%s </b><br><i>%s </i><br>Release Date : %s" % (row[PRE_ARTIST], row[PRE_TITLE], street_date_formatted_for_america)
                product.product_type = "LP"#default for now, might change later
                product.tags = row[PRE_SHOPIFY_TAGS]
                
                #build description
                desc = '<b>UPC: %s </b><br>' % row[PRE_UPC]
                if len(row[PRE_LABEL]) > 1:
                    desc += 'Label: %s <br>' % row[PRE_LABEL]
                desc += 'Format: %s <br>' % row[PRE_FORMAT]
                if len(row[PRE_STREET_DATE]) > 1:
                    desc += 'Release Date: %s <br>' % row[PRE_STREET_DATE]
                desc += '<br>'
                #new_product.body_html = '<b>UPC: %s </b><br>Format: %s <br>Label: In stock items ship within 24 hours.'
                product.body_html = desc + row[PRE_SHOPIFY_DESC]

                
                #product.body_html = row[PRE_SHOPIFY_DESC]
                product.metafields_global_title_tag = "Pre-Order %s %s" % (row[PRE_ARTIST], row[PRE_TITLE])
                product.metafields_global_description_tag = "Pre-order now from an independently owned record store in Cincinnati, OH %s" % (row[PRE_UPC])
                if row[PRE_ACTIVE] == 0:
                    product.published_at = None
                else:
                    product.published_at = datetime.datetime.now().isoformat()
                product.published_scope = 'web'
                #v = shopify.Variant()
                v = product.variants[0]
                v.price = row[PRE_SALE_PRICE]
                v.sku = row[PRE_UPC]
                v.product_id = product.id
                v.weight = 500
                v.weight_unit = 'lb'
                #new_product.variants = [v]
                success = product.save()
                #pprint (vars(new_product))
                #print
            except Exception as e:
                print 'error in the shopify:create_or_update_item func (UPDATE): %s' % e
                return None
            if success == False:
                return None
            time.sleep(0.5)
            return product

        
            
        
        
#if __name__ == '__main__':
#    shopify_interface = ShopifyInterface()
#    orders = shopify.Order.find()
    
    
    #for order in orders:
    #    details = shopify.Order.get(shopify.Order.get_id(order))
    #    print details['shipping_address']

#    upcs = set()
#    for row in shopify_interface.db_cursor.execute('SELECT * FROM inventory WHERE new_used = ? ORDER BY date_added DESC LIMIT 250', ('New',)):
#        if row[UPC_INDEX] in upcs:
#            time.sleep(1)
#            continue
#        new_product = shopify.Product()
#        new_product.title = "<b>%s</b><br><i>%s</i>" % (row[ARTIST_INDEX], row[TITLE_INDEX])
#        new_product.product_type = "LP"
#        new_product.tags = "Format_LP,Pre-Order_09/23/16,Pre-Orders"
#        v = shopify.Variant()
#        v.price = row[PRICE_INDEX]
#        v.barcode = row[UPC_INDEX]
#        v.product_id = new_product.id
#        new_product.variants = [v]
#        success = new_product.save()
#        time.sleep(1)
#        upcs.add(row[UPC_INDEX])
        
        
