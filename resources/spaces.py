from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse, 
							inputs, fields,
							marshal, marshal_with,
							url_for
							)

import models

space_fields = {
	'id': fields.Integer,
	'field_values': fields.String
}

def parse_field_values(field_values):
	field_values.strip().split(",")

def space_or_404(space_id):
	try:
		space = models.Space.get(models.Space.id==space_id)
	except models.Space.DoesNotExist:
		abort(404)
	else:
		return space


class SpaceList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'field_values',
			required=True,
			help='No field_values provided',
			location=['form', 'json']
		)
		
		super().__init__()



	def get(self):
		spaces = [marshal(space, space_fields)
				for space in models.Space.select()]
		return {'spaces': spaces}

	@marshal_with(space_fields)
	def post(self):
		args = self.reqparse.parse_args()
		space = models.Space.create(**args)
		return (space, 201, {
			'Location': url_for('resources.spaces.space', id=space.id)
			})



# for individual space
class Space(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'field_values',
			required=True,
			help='No field_values provided',
			location=['form', 'json']
		)
		

		super().__init__()



	@marshal_with(space_fields)
	def get(self, id):
		return space_or_404(id)

	# patch can update only one arg, put takes all args
	@marshal_with(space_fields)
	def put(self, id):
		args = self.reqparse.parse_args()
		query = models.Space.update(**args).where(models.Space.id==id)
		query.execute()
		return (models.Space.get(models.Space.id==id), 200, 
				{'Location': url_for('resources.spaces.space', id=id)})
	
	def delete(self, id):
		query = models.Space.delete().where(models.Space.id==id)
		query.execute()
		return '', 204, {'Location': url_for('resources.spaces.spaces')}


spaces_api = Blueprint('resources.spaces', __name__)
api = Api(spaces_api)
api.add_resource(
	SpaceList,
	'/api/v1/spaces',
	endpoint='spaces'
)
api.add_resource(
	Space,
	'/api/v1/spaces/<int:id>',
	endpoint='space'
)