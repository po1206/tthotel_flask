from flask import Blueprint, render_template, jsonify, request


passcode_bp = Blueprint('passcode', __name__, url_prefix='/passcode')

@passcode_bp.route('/')
def index():
    
    return render_template('passcode.html', current_route='passcode')

@passcode_bp.route('/data', methods=["GET"])
def data():
    from model.passcode import getPasscode
    
    owner = request.args.get('owner', default='')
    startDate = request.args.get("startDate", default=-1)
    endDate = request.args.get('endDate', default=-1)
    accessto = request.args.get('accessto', default='')
    
    result = getPasscode( owner, startDate, endDate, accessto)
    
    return jsonify(result)