from random import randint
from flask import Flask, jsonify
from flask_cors import CORS
import logging
import sys
import requests
from ddtrace import tracer



application = Flask(__name__)
cors = CORS(application)

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


@application.route("/rolldice")
def roll_dice():
    with tracer.trace("roll_dice", resource="roll_dice_resource") as span:
        trace_id = ""
        temp = do_roll()
        if temp==6:
            trace_id = random_cat()
        else:
            trace_id = span.trace_id
        return jsonify({"dice": temp, "trace": trace_id}), 200

    # with tracer.start_as_current_span("roll_dice"):
    #     print("Rolling dice")
    #     return jsonify({"dice": do_roll(), "trace": span.trace_id}), 200

def do_roll():
    logging.info("Doing the roll... roll... roll... roll...")
    return randint(1, 6)

def random_cat():
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    cat_image = response.json()[0]['url']
    return cat_image


# @application.route("/getRequest", methods=['GET'])
# def get_request():
#     logging.info("GET request received")
#     return "success", 200


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5500)
