from random import randint
from flask import Flask, jsonify
from flask_cors import CORS
import requests
from opentelemetry import trace
# from opentelemetry.instrumentation.flask import FlaskInstrumentor

application = Flask(__name__)
cors = CORS(application)
tracer = trace.get_tracer(__name__)

# FlaskInstrumentor().instrument_app(application)

@application.route("/rolldice")
def roll_dice():
    with tracer.start_as_current_span("roll_dice"):
        trace_id = ""
        temp = do_roll()
        if temp==6:
            trace_id = random_cat()
        else:
            trace_id = str(trace.get_current_span().get_span_context().trace_id)
        return jsonify({"dice": temp, "trace": trace_id}), 200

    # with tracer.start_as_current_span("roll_dice"):
    #     print("Rolling dice")
    #     return jsonify({"dice": do_roll(), "trace": span.trace_id}), 200

def do_roll():
    return randint(1, 6)

def random_cat():
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    cat_image = response.json()[0]['url']
    return cat_image


@application.route("/getRequest", methods=['GET'])
def get_request():
    return "success", 200