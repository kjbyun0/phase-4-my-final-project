from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from config import db, bcrypt

# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-_password_hash', '-job_openings.employer',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    mobile = db.Column(db.String)
    phone = db.Column(db.String)
    street_1 = db.Column(db.String)
    street_2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.String) # => Maybe want to validate it

    job_openings = db.relationship('JobOpening', back_populates='employer', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.id}, {self.username}>'
    
    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
    
    @validates('email', 'mobile', 'phone', 'zip_code')
    def validate(self, key, value):
        if key == 'email':
            if '@' not in value:
                raise ValueError('Server validation Error: Invalid email address')
        elif key == 'mobile' or key == 'phone':
            if len(value) != 0 and (len(value) != 12 or value.find(')') != 3 or \
                value.find('-') != 7 or not value[:3].isdecimal() or 
                not value[4:7].isdecimal() or not value[-4:].isdecimal()):
                raise ValueError(f'Server validation error: Invalid {key} number')
        elif key == 'zip_code':
            if len(value) != 5 or not value.isdecimal():
                raise ValueError('Server validation error: Invalid zip code')
        return value

class JobCategory(db.Model, SerializerMixin):
    __tablename__ = 'job_categories'

    serialze_rules = ('-job_openings.job_category',)

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    
    job_openings = db.relationship('JobOpening', back_populates='job_category', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<JobCategory {self.id}, {self.category}>'
    
class JobOpening(db.Model, SerializerMixin):
    __tablename__ = 'job_openings'

    serialize_rules = ('-job_category.job_openings', '-employer.job_openings')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    salary = db.Column(db.Float, nullable=False)
    job_type = db.Column(db.String) # => full,partime,contract
    location = db.Column(db.String, nullable=False) 
    remote = db.Column(db.String, nullable=False)   # => On Site, Remote, Hybrid
    isActive = db.Column(db.Boolean, nullable=False)

    # skills,

    job_category_id = db.Column(db.Integer, db.ForeignKey('job_categories.id'))
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    job_category = db.relationship('JobCategory', back_populates='job_openings')
    employer = db.relationship('User', back_populates='job_openings')
    
    def __repr__(self):
        return f'<JobOpening {self.id} {self.title}>'

