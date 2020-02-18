from argparse import ArgumentParser
from flask import Flask, jsonify

oracle = Flask(__name__)

@oracle.route('/backdata',methods = ['GET'])
def back_data():
    return jsonify('speed'),200


if __name__=='__main__':
    parser=ArgumentParser()
    parser.add_argument('-p', '--port', default=8000, help='input your using port')
    args=parser.parse_args()
    port=args.port
    oracle.run(host='0.0.0.0', port=port, debug=True)