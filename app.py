from flask import Flask, render_template, redirect, url_for, request, make_response
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
    
class Services(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    mins = db.Column(db.Integer, nullable=False)

    def __init__(self, company_id, name, description, hours, mins):
        self.company_id = company_id
        self.name = name
        self.description = description
        self.hours = hours
        self.mins = mins

    def __repr__(self):
        return f"{self.name}, {self.description}, {self.hours}, {self.mins}"
    
class Bookings(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    

    def __init__(self, company_id, service_id, name, phone, email, date):
        self.company_id = company_id
        self.service_id = service_id
        self.name = name
        self.phone = phone
        self.email = email
        self.date = date

    def __repr__(self):
        return f"{self.company_id}, {self.service_id}, {self.name}, {self.phone}, {self.email}, {self.date}"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']

        if not username:
            return redirect(url_for('index'))
        
        company = Company.query.filter_by(name=username).first()
        if company:
            return redirect(f"/dashboard/{company.id}")

        
        return redirect(url_for('index'))


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

        return redirect(f"/dashboard/{company_id}")
    else:
        return redirect(url_for('register_name'))
    
@app.route('/dashboard/<int:company_id>')
def dashboard(company_id):

    company = Company.query.get(company_id)
    bookings = Bookings.query.filter_by(company_id=company_id).all()
    bookings_today = bookings_thisWeek = len(bookings)
    workLoad = [0, 0]
    revenue = 0
    visits = 0

    desingedBookings = []

    for booking in bookings:
        service = Services.query.get(booking.service_id)
        workLoad[0] += service.hours
        workLoad[1] += service.mins
        print(workLoad)
        revenue += service.hours * 96

        desingedBookings.append({
            'name': booking.name,
            'phone': booking.phone,
            'email': booking.email,
            'date': booking.date,
            'company_name': company.name,
            'service_name': service.name
        })

    return render_template('dashboard.html', company_id=company_id, bookings=desingedBookings, bookings_today=bookings_today, bookings_thisWeek=bookings_thisWeek, workLoad=workLoad, revenue=revenue, visits=visits)

@app.route('/manage-items/<int:company_id>', methods=['POST', 'GET'])
def manage_items(company_id):
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        hours = request.form.get('hours')
        mins = request.form.get('minutes')

        if not name or not description or not hours or not mins:
            return redirect(f"/manage-items/{company_id}")
        
        service = Services(company_id=company_id, name=name, description=description, hours=hours, mins=mins)
        db.session.add(service)
        db.session.commit()

        return redirect(f"/manage-items/{company_id}")
    else:
        services = Services.query.filter_by(company_id=company_id).all()
        return render_template('manage-items.html', company_id=company_id, services=services)

@app.route('/booking/home/<int:company_id>')
def booking_home(company_id):
    company = Company.query.get(company_id)
    company_location = CompanyAddress.query.filter_by(company_id=company_id).first()

    return render_template('home.html', company=company, company_location=company_location)

@app.route('/booking/book/<int:company_id>', methods=['POST', 'GET'])
def booking_book(company_id):
    if request.method == "POST":
        pass
    else:
        services = Services.query.filter_by(company_id=company_id).all()

        return render_template('book-now.html', company_id=company_id, services = services)
    
@app.route('/booking/confirm/<int:service_id>/<int:company_id>', methods=['POST', 'GET'])
def booking_confirm(service_id, company_id):
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        date = request.form.get('date')

        if not name or not phone or not email or not date:
            return redirect(f"/booking/book/{company_id}")
        
        booking = Bookings(company_id=company_id, service_id=service_id, name=name, phone=phone, email=email, date=date)
        db.session.add(booking)
        db.session.commit()

        return redirect(f"/booking/summary/{booking.id}/{company_id}")
    else:
        Service = Services.query.get(service_id)
        company = Company.query.get(company_id)

        return render_template('confirm-booking.html', service=Service, company=company)
    
@app.route('/booking/summary/<int:booking_id>/<int:company_id>')
def booking_summary(booking_id, company_id):
    booking  = Bookings.query.get(booking_id)
    service_id = booking.service_id
    service = Services.query.get(service_id)

    return render_template('summary.html', service=service, booking=booking, company_id=company_id)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)