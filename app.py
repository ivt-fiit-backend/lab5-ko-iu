import json
from flask import Flask, abort, jsonify, request
from flask_restx import Api

PAGE_SIZE = 25

app = Flask(__name__)
api = Api(app)

with open('awards.json', encoding='utf-8') as f:
    awards = json.load(f)

with open('laureats.json', encoding='utf-8') as f:
    laureats_data = json.load(f)
    if isinstance(laureats_data, dict) and 'laureates' in laureats_data:
        laureats = laureats_data['laureates']
    elif isinstance(laureats_data, list):
        laureats = laureats_data
    else:
        laureats = []


@app.route("/api/v1/awards/")
def awards_list():
    try:
        p = int(request.args.get('p', 0))
        if p < 0:
            raise ValueError
    except ValueError:
        return abort(400)
    page = awards[p * 50:(p + 1) * 50]
    return jsonify({
        'page': p,
        'count_on_page': PAGE_SIZE,
        'total': len(awards),
        'items': page,
    })


@app.route("/api/v1/award/<int:pk>/")
def award_object(pk):
    if 0 <= pk < len(awards):
        return jsonify(awards[pk])
    else:
        abort(404)


@app.route("/v2/laureats/")
def laureats_list():
    return jsonify(laureats)


@app.route("/v2/laureat/<string:id>/")
def laureat_by_id(id):
    for laureat in laureats:
        if laureat['id'] == id:
            return jsonify(laureat)
    abort(404, description=f"Лауреат с id {id} не найден")


if __name__ == '__main__':
    app.run(debug=True)
