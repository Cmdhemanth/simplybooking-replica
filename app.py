from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'

db = SQLAlchemy(app)

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)

    def __init__(self, name, phone, category):
        self.name = name
        self.phone = phone
        self.category = category

    def __repr__(self):
        return f"{self.name}, {self.phone}, {self.category}"
    
class CompanyAddress(db.Model):
    __tablename__ = 'company_addresses'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    address = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)

    def __init__(self, company_id, address, city, state, country):
        self.company_id = company_id
        self.address = address
        self.city = city
        self.state = state
        self.country = country

    def __repr__(self):
        return f"{self.company_id}, {self.address}, {self.city}, {self.state}, {self.country}"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register')
def register_name():
    return render_template('register-name.html')

@app.route('/register-name-save', methods=['POST'])
def register_location():
    if request.method == 'POST':
        company = request.form['company']
        phone = request.form['phone']
        category = request.form.get('category')

        if not company or not phone or not category:
            return redirect(url_for('register_name'))
        
        company = Company(name=company, phone=phone, category=category)
        db.session.add(company)
        db.session.commit()

        return redirect(f"/register-location/{company.id}")
    return redirect(url_for('register_name'))

@app.route('/register-location/<int:company_id>')
def registar_final(company_id):
    return render_template('register-location.html', company_id=company_id)

@app.route('/register-complete/<int:company_id>', methods=['POST'])
def register_complete(company_id):
    if request.method == 'POST':
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')

        if not address or not city or not state or not country:
            return redirect(url_for('register_location'))
        
        address = CompanyAddress(company_id=company_id, address=address, city=city, state=state, country=country)
        db.session.add(address)
        db.session.commit()

        return render_template('register-complete.html', address=address)
    else:
        return redirect(url_for('register_name'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)