from exts import db


class Pharmacy(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    adress = db.Column(db.String(), nullable = False)
    number = db.Column(db.String(20), nullable = False)
    scrapped_at = db.Column(db.DateTime(), nullable = False)
    province = db.Column(db.String(50), nullable=False)

    
    
    
    def __repr__(self):
        pass
    
    