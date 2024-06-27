from exts import db


class Pharmacy(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    adress = db.Column(db.String(), nullable = False)
    number = db.Column(db.String(20), nullable = False)
    scrapped_at = db.Column(db.DateTime(), nullable = True)
    province = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<adress {self.adress}>"
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self, name, adress, number, scrapped_at, province):
        self.name = name
        self.adress = adress
        self.number = number
        self.scrapped_at = scrapped_at
        self.province = province
        db.session.commit()
        
        
class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    username=db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text(), nullable = False)
    def __repr__(self):
        return f"<User {self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
