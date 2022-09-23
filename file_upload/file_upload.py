from flask import request, Blueprint

file_import_page = Blueprint('file_import_page', __name__, template_folder='templates')


@file_import_page.route('/csv', methods=['POST'])
def import_csv():
    data = request.get_json()
    print("csv successfully imported!")
