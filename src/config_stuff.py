UPC_INDEX = 0
ARTIST_INDEX = 1
TITLE_INDEX = 2
FORMAT_INDEX = 3
PRICE_INDEX = 4
PRICE_PAID_INDEX = 5
NEW_USED_INDEX = 6
DISTRIBUTOR_INDEX = 7
LABEL_INDEX = 8
GENRE_INDEX = 9
YEAR_INDEX = 10
DATE_ADDED_INDEX = 11
DISCOGS_RELEASE_NUMBER_INDEX = 12
REAL_NAME_INDEX = 13
PROFILE_INDEX = 14
VARIATIONS_INDEX = 15
ALIASES_INDEX = 16
TRACK_LIST_INDEX = 17
NOTES_INDEX = 18
TAXABLE_INDEX = 19
RESERVED_ONE_INDEX = 20
RESERVED_TWO_INDEX = 21
ID_INDEX = 22
SOLD_FOR_INDEX = 23
PERCENT_DISCOUNT_INDEX = 24
DATE_SOLD_INDEX = 25
SOLD_NOTES_INDEX = 26
REORDER_STATE_INDEX = 27
TRANSACTION_ID_INDEX = 28
RESERVED_THREE_INDEX = 29 
NEW_ID_INDEX = 30

MISC_UPC_INDEX = 0
MISC_TYPE_INDEX = 1
MISC_ITEM_INDEX = 2
MISC_DESCRIPTION_INDEX = 3
MISC_SIZE_INDEX = 4
MISC_PRICE_INDEX = 5
MISC_PRICE_PAID_INDEX = 6
MISC_DATE_ADDED_INDEX = 7
MISC_NEW_USED_INDEX = 8
MISC_CODE_INDEX = 9
MISC_DISTRIBUTOR_INDEX = 10
MISC_TAXABLE_INDEX = 11
MISC_RESERVED_ONE_INDEX = 12
MISC_RESERVED_TWO_INDEX = 13
MISC_RESERVED_THREE_INDEX = 14
MISC_RESERVED_FOUR_INDEX = 15
MISC_ID_INDEX = 16
MISC_SOLD_FOR_INDEX = 17
MISC_PERCENT_DISCOUNT_INDEX = 18
MISC_DATE_SOLD_INDEX = 19
MISC_SOLD_NOTES_INDEX = 20
MISC_REORDER_STATE_INDEX = 21
MISC_TRANSACTION_ID_INDEX = 22
MISC_RESERVED_FIVE_INDEX = 23
MISC_RESERVED_SIX_INDEX = 24
MISC_NEW_ID_INDEX = 25

TRANS_NUMBER_OF_ITEMS_INDEX = 0
TRANS_DATE_SOLD_INDEX = 1
TRANS_SUBTOTAL_INDEX = 2
TRANS_DISCOUNT_PERCENT_INDEX = 3
TRANS_DISCOUNTED_PRICE_INDEX = 4
TRANS_TAX_INDEX = 5
TRANS_SHIPPING_INDEX = 6
TRANS_TOTAL_INDEX = 7
TRANS_CASH_CREDIT_INDEX = 8
TRANS_SOLD_INVENTORY_IDS_INDEX = 9
TRANS_SOLD_MISC_INVENTORY_IDS_INDEX = 10
TRANS_TENDERED_INDEX = 11
TRANS_CHANGE_INDEX = 12
TRANS_RESERVED_ONE_INDEX = 13
TRANS_RESERVED_TWO_INDEX = 14
TRANS_RESERVED_THREE_INDEX = 15
TRANS_RESERVED_FOUR_INDEX = 16
TRANS_ID_INDEX = 17

COLE_BUSINESS_NAME_INDEX = 0
COLE_CONTACT_NAME_INDEX = 1
COLE_PHONE_INDEX = 2
COLE_CELL_INDEX = 3
COLE_EMAIL_INDEX = 4
COLE_BILLING_NAME_INDEX = 5
COLE_BILLING_LINE_ONE_INDEX = 6
COLE_BILLING_LINE_TWO_INDEX = 7
COLE_BILLING_LINE_THREE_INDEX = 8
COLE_BILLING_CITY_INDEX = 9
COLE_BILLING_STATE_INDEX = 10
COLE_BILLING_ZIP_INDEX = 11
COLE_BILLING_COUNTRY_INDEX = 12
COLE_SHIPPING_NAME_INDEX = 13
COLE_SHIPPING_LINE_ONE_INDEX = 14
COLE_SHIPPING_LINE_TWO_INDEX = 15
COLE_SHIPPING_LINE_THREE_INDEX = 16
COLE_SHIPPING_CITY_INDEX = 17
COLE_SHIPPING_STATE_INDEX = 18
COLE_SHIPPING_ZIP_INDEX = 19
COLE_SHIPPING_COUNTRY_INDEX = 20
COLE_NOTES_INDEX = 21
COLE_ACCOUNT_NUMBER_INDEX = 22

COLE_INV_UPC_INDEX = 0
COLE_INV_QTY_INDEX = 1
COLE_INV_CATALOG_INDEX = 2
COLE_INV_ARTIST_INDEX = 3
COLE_INV_TITLE_INDEX = 4
COLE_INV_FORMAT_INDEX = 5
COLE_INV_WHOLESALE_INDEX = 6
COLE_INV_COST_INDEX = 7
COLE_INV_LABEL_INDEX = 8
COLE_INV_ID_INDEX = 9
COLE_INV_QTY_ORDERED_INDEX = 10
COLE_INV_QTY_BO_INDEX = 11
COLE_INV_QTY_SHIPPED_INDEX = 12
COLE_INV_PRICE_INDEX = 13
COLE_INV_DATE_SOLD_INDEX = 14
COLE_INV_TRANS_ID_INDEX = 15
COLE_INV_ACCOUNT_NO_INDEX = 16
COLE_INV_STATUS_INDEX = 17
COLE_INV_NEW_ID_INDEX = 18

COLE_TRANS_NO_ITEMS_INDEX = 0
COLE_TRANS_DATE_INDEX = 1
COLE_TRANS_SUBTOTAL_INDEX = 2
COLE_TRANS_SHIPPING_INDEX = 3
COLE_TRANS_DISCOUNT_INDEX = 4
COLE_TRANS_TOTAL_INDEX = 5
COLE_TRANS_SOLD_IDS_INDEX = 6
COLE_TRANS_ACCOUNT_NO_INDEX = 7
COLE_TRANS_PAYPAL_TRANS_INDEX = 8
COLE_TRANS_PAYPAL_TRANS_ID_INDEX = 9
COLE_TRANS_NOTES_INDEX = 10
COLE_TRANS_STATUS_INDEX = 11
COLE_TRANS_ID_INDEX = 12

BOOKS_DATE_INDEX = 0
BOOKS_AMOUNT_INDEX = 1
BOOKS_CATEGORY_INDEX = 2
BOOKS_COMPANY_INDEX = 3
BOOKS_RELEASE_INDEX = 4
BOOKS_DETAILS_INDEX = 5
BOOKS_BATCH_INDEX = 6
BOOKS_DATE_ADDED_INDEX = 7
BOOKS_ID_INDEX = 8

NEEDS_REORDERED = 0
ON_CURRENT_PO_LIST = 1
REORDERED = 2
NOT_REORDERING = 3

NEEDS_PUT_OUT = 0
ALREADY_OUT = 1

DRAFT = 0
SENT = 1
PAID = 2

#/Users/bccole1989/Documents/plaid_room_records/add_tabs/plaid_room
#BASE_PATH = '/Users/bccole1989/Documents/plaid_room_records/add_tabs/'
BASE_PATH = '/Users/plaidroomrecords/Documents/pos_software/'
#BASE_PATH = '/Volumes/NAS-250GB/pos_software/'

#config stuff for all kinds of combo boxes
DIST_FILE_NAME = BASE_PATH + 'plaid_room/config/distributors.csv'
MISC_TYPES_FILE_NAME = BASE_PATH + 'plaid_room/config/misc_types.csv'
MISC_DIST_FILE_NAME = BASE_PATH + 'plaid_room/config/misc_distributors.csv'
TEMP_RECEIPT_FILE_NAME = BASE_PATH + 'plaid_room/images/receipt_test.pdf'
RECEIPT_HEADER_FILE_NAME = BASE_PATH + 'plaid_room/images/plaid_room.jpg'
BABY_LOGO_FILE_NAME = BASE_PATH + 'plaid_room/images/baby_logo.jpg'
PAYPAL_FILE_NAME = BASE_PATH + 'plaid_room/config/paypal.key'
DB_FILE = BASE_PATH + 'plaid_room/real_inventory.db'
EMAIL_PASSWORD_FILE_NAME = BASE_PATH + 'plaid_room/config/password.email'
CATALOGS_PATH = BASE_PATH + 'plaid_room/config/catalogs/'
SHOPIFY_COLEMINE_NAME = BASE_PATH + 'plaid_room/config/colemine_shopify.key'
SHOPIFY_PLAID_ROOM_NAME = BASE_PATH + 'plaid_room/config/plaid_room_shopify.key'
PAYPAL_LOGIN_NAME = BASE_PATH + 'plaid_room/config/paypal_login.key'


#other stuff
LOVELAND_TAX_RATE = 6.75 #percent
DESIRED_PROFIT_MARGIN = 30
DEFAULT_PRICE = 1.00
