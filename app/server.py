from flask import Flask, request, jsonify

from app import utils
from app.scanners import owasp, sourceclear

import subprocess


server = Flask(__name__)


@server.route("/")
def hello():
    return "Hello World!"


@server.route("/efda/list")
def list_efda():
    return jsonify(utils.find_efda_projects("efda"))


@server.route("/scan/owasp", methods=["POST"])
def scan_owasp():
    target = request.form["target"]
    project_paths = utils.find_efda_projects("efda")

    if target not in project_paths:
        abort(404)
    else:
        return jsonify(owasp.scan(target))


@server.route("/scan/srcclr", methods=["POST"])
def scan_srcclr():
    target = request.form["target"]
    project_paths = utils.find_efda_projects("efda")

    if target not in project_paths:
        abort(404)
    else:
        try:
            return jsonify(sourceclear.scan(target))
        except subprocess.CalledProcessError as e:
            ret = {}
            ret["err_msg"] = e.stderr.decode()

            return jsonify(ret), 500