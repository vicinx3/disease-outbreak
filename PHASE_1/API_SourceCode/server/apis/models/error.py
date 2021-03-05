from flask_restplus import Model, fields

model = Model('Error', {
	'message': fields.String(description='Error message.', example='Format of \'end_date\' is invalid')
})