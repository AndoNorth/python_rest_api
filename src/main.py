from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return "Video(name = "+self.name
        +", likes = "+str(self.likes)
        +", views = "+str(self.views)+")"

# db.create_all() # initialize database if it doesnt exist

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="name of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="likes on the video is required", required=True)
video_put_args.add_argument("views", type=int, help="views on the video is required", required=True)

video_patch_args = reqparse.RequestParser()
video_patch_args.add_argument("name", type=str, help="name of the video")
video_patch_args.add_argument("likes", type=int, help="likes on the video")
video_patch_args.add_argument("views", type=int, help="views on the video")


resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'likes' : fields.Integer,
    'views' : fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields) # this can be added to any method, it ensures objects return match the format defined
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="could not find video with that id")

        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="video id already taken...")

        video = VideoModel(id=video_id,
                            name=args['name'],
                            views=args['views'],
                            likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_patch_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video does not exist, cannot update")
        
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()
        return result


    def delete(self, video_id):
        args = video_patch_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video does not exist, cannot delete")

        db.session.delete(result)
        db.session.commit()
        return '', 204


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)