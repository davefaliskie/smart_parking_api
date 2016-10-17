from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse, 
							inputs, fields,
							marshal, marshal_with,
							url_for
							)

import models

lot_fields = {
	'id': fields.Integer,
	'field_values': fields.String,
	'reader_Name': fields.String
}

def lot_or_404(lot_id):
	try:
		lot = models.Lot.get(models.Lot.id==lot_id)
	except models.Lot.DoesNotExist:
		abort(404)
	else:
		return lot


class LotList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'reader_Name',
			required=True,
			help='No reader_Name provided',
			location=['form', 'json']
		)

		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'field_values',
			required=True,
			help='No field_values provided',
			location=['form', 'json']
		)

		super().__init__()



	def get(self):
		lots = [marshal(lot, lot_fields)
				for lot in models.Lot.select()]
		return {'lots': lots}

	@marshal_with(lot_fields)
	def post(self):
		args = self.reqparse.parse_args()
		lot = models.Lot.create(**args)
		return (lot, 201, {
			'Location': url_for('resources.lots.lot', id=lot.id)
			})



# for individual lot
class Lot(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'reader_Name',
			required=True,
			help='No reader_Name provided',
			location=['form', 'json']
		)

		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'field_values',
			required=True,
			help='No field_values provided',
			location=['form', 'json']
		)

		super().__init__()



	@marshal_with(lot_fields)
	def get(self, id):
		return lot_or_404(id)

	# patch can update only one arg, put takes all args
	@marshal_with(lot_fields)
	def put(self, id):
		args = self.reqparse.parse_args()
		query = models.Lot.update(**args).where(models.Lot.id==id)
		query.execute()
		return (models.Lot.get(models.Lot.id==id), 200, 
				{'Location': url_for('resources.lots.lot', id=id)})
	
	def delete(self, id):
		query = models.Lot.delete().where(models.Lot.id==id)
		query.execute()
		return '', 204, {'Location': url_for('resources.lots.lots')}


lots_api = Blueprint('resources.lots', __name__)
api = Api(lots_api)
api.add_resource(
	LotList,
	'/api/v1/lots',
	endpoint='lots'
)
api.add_resource(
	Lot,
	'/api/v1/lots/<int:id>',
	endpoint='lot'
)