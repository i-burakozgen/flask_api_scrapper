from flask import Flask
from flask_restx import Api, Resource 
from config import DevConfig
from exts import db
from models import Pharmacy
from flask_migrate import Migrate



app = Flask(__name__)
app.config.from_object(DevConfig)
api = Api(app, doc="/docs")
db.init_app(app)
migrate = Migrate(app, db)


def create_tables():
    db.create_all()

@api.route("/pharmacies/<string:province>")
class PharmacyByProvince(Resource):
    def get(self, province):
        pharmacies = Pharmacy.query.filter_by(province=province).all()
        return [{
            "name": pharmacy.name,
            "adress": pharmacy.adress,
            "number": pharmacy.number,
            "scrapped_at": pharmacy.scrapped_at.strftime('%Y-%m-%d %H:%M:%S'),
            "province": pharmacy.province
        } for pharmacy in pharmacies], 200


    

if __name__ == "__main__":
    app.run()

