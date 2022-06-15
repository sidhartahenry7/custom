{
    'name': 'Toko Baju',  #nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Henry',
    'summary': 'Modul Toko Baju UAS Konfigurasi ERP', #deskripsi singkat dari modul
    'description': 'Ideas management module', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    #di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base', 'hr', 'sale', 'sales_team'],  # list of dependencies, conditioning startup order
    'data': [
        'security/ir.model.access.csv',
        'views/membership_views.xml',
        'views/employee_views.xml',
        'views/produk_views.xml',
        'views/kategori_views.xml',
        'views/brand_views.xml',
        'views/diskon_views.xml',
        'views/transaksi_views.xml',
        'wizard/wiz_tokobaju_transaksi_views.xml',
        'data/ir_sequence_data.xml',
    ],
    'qweb':[],  #untuk memberi tahu static file, misal CSS
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}