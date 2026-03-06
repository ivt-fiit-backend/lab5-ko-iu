import json
from flask import Flask, abort, jsonify, request
from flask_restx import Api, Resource  # type: ignore

PAGE_SIZE = 25

app = Flask(__name__)
api = Api(app)
ns = api.namespace("v2", description="Laureats API")

with open("awards.json", encoding="utf-8") as f:
    awards = json.load(f)

with open("laureats.json", encoding="utf-8") as f:
    laureats_data = json.load(f)

if isinstance(laureats_data, dict) and "laureates" in laureats_data:
    laureats = laureats_data["laureates"]
else:
    laureats = laureats_data


@app.route("/api/v1/awards/")
def awards_list():
    try:
        p = int(request.args.get("p", 0))
        if p < 0:
            raise ValueError
    except ValueError:
        abort(400)

    page = awards[p * PAGE_SIZE:(p + 1) * PAGE_SIZE]

    return jsonify({
        "page": p,
        "count_on_page": PAGE_SIZE,
        "total": len(awards),
        "items": page,
    })


@app.route("/api/v1/award/<int:pk>/")
def award_object(pk):
    if 0 <= pk < len(awards):
        return jsonify(awards[pk])
    abort(404)


@ns.route("/laureats/")
class LaureatsList(Resource):

    def get(self):
        return jsonify(laureats)


@ns.route("/laureat/<string:pk>/")
class LaureatObject(Resource):

    def get(self, pk):
        for laureat in laureats:
            if laureat.get("id") == pk:
                return jsonify(laureat)
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)
