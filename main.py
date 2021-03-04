from flask import Flask, request
from app import app
from flask_marshmallow import Marshmallow
from app.models import Data
from flask_restful import Api, Resource
import time
from app import db

db.create_all()
ma = Marshmallow(app)
api = Api(app)


class DataSchema(ma.Schema):
	'''
	Displays the json string after a successful record creation
	'''
	class Meta:
		fields = ("id", "timestamp", "value1","value2","value3")


post_schema = DataSchema()
posts_schema = DataSchema(many=True)


class ListRecords(Resource):
	'''
	Class to handle list requests
	'''
	def get(self):
		posts = Data.query.all()
		return posts_schema.dump(posts)

	
class CreateRecord(Resource):
	'''
	Class to handle create requests
	'''
	def post(self):
		new_post = Data(
			timestamp = request.json['timestamp'],
			value1=request.json['value1'],
			value2=request.json['value2'],
			value3=request.json['value3'],
			creationDate = time.time(),
			lastModificationDate = time.time()

		)
		db.session.add(new_post)
		db.session.commit()
		return post_schema.dump(new_post)

class ReadRecord(Resource):
	'''
	Class to handle read requests specified by some id
	'''
	def get(self, post_id):
		post = Data.query.get_or_404(post_id)
		return post_schema.dump(post)

class ModifyRecord(Resource):
	'''
	Class to handle update requests
	'''
	def patch(self, post_id):
		post = Data.query.get_or_404(post_id)

		if 'timestamp' in request.json:
			post.timestamp = request.json['timestamp']
		if 'value1' in request.json:
			post.value1 = request.json['value1']
		if 'value2' in request.json:
			post.value2 = request.json['value2']
		if 'value3' in request.json:
			post.value3 = request.json['value3']
		
		post.lastModificationDate = time.time()

		db.session.commit()
		return post_schema.dump(post)


class RemoveRecord(Resource):
	'''
	Class to handle delete requests
	'''
	def delete(self, post_id):
		post = Data.query.get_or_404(post_id)
		db.session.delete(post)
		db.session.commit()
		return '', 204

	

	

# Routes to the REST Apis
api.add_resource(ListRecords, '/api/list')
api.add_resource(CreateRecord, '/api/create')
api.add_resource(ReadRecord, '/api/read/<int:post_id>')
api.add_resource(ModifyRecord, '/api/modify/<int:post_id>')
api.add_resource(RemoveRecord, '/api/remove/<int:post_id>')



