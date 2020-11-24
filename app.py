from flask import Flask, request
from flask_cors import CORS
from flask import jsonify
import grammar
import shared_vm

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    print('Entered Home')
    response = "this is response"
    return jsonify(response)


@app.route('/compile', methods=['POST'])
def compile():

    code = request.get_json()

    mobile_code_file = open('mobile_code.ap', 'w')
    mobile_code_file.write(code)
    mobile_code_file.close()

    grammar.comp_and_run('mobile_code.ap')
    return jsonify(shared_vm.output)