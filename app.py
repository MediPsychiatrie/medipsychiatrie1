from flask import Flask, request, jsonify, render_template, redirect, url_for, session, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import uuid 
from collections import defaultdict
from main import get_response, chat_history
from datetime import datetime


# Initialiser Firebase
cred = credentials.Certificate("static\json\medipsychiatre-d9468-firebase-adminsdk-wkpmq-be65e67b62.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__, static_url_path='/static')

app.secret_key = 'gjsgft678gHRt4KQDgdqjddv17hsdALKnxixs'



#----Firebase---------------------------------------------------------------------


# Route pour gérer la soumission du formulaire
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        genre = request.form['Genre']
        date_naissance = request.form['date']
        situation_familiale = request.form['Situation_Familiale']
        poids = request.form['poids']
        taille = request.form['taille']
        email = request.form['your_email']
        password = request.form['password']
        phone = request.form['phone']
        place = request.form['place']
        country = request.form['country']


        # Enregistrer les données dans Firestore
        doc_ref = db.collection('users').document()
        doc_ref.set({
            'first_name': first_name,
            'last_name': last_name,
            'genre': genre,
            'date_naissance': date_naissance,
            'situation_familiale': situation_familiale,
            'poids': poids,
            'taille': taille,
            'email': email,
            'password': password,
            'phone': phone,
            'place': place,
            'country': country
        })
        return 'Data has been successfully submitted to Firebase!'
    else:
        return 'Invalid request method'

#---------------------------Registration-------------------------------------------------------

@app.route('/registration', methods=['POST'])
def registration():
    # Get form data
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    genre = request.form['Genre']
    date_of_birth = request.form['date']
    marital_status = request.form['Situation_Familiale']
    poids = request.form['poids']
    taille = request.form['taille']
    email = request.form['your_email']
    password = request.form['password']
    phone = request.form['phone']
    place = request.form['place']
    country = request.form['country']

    # Process the data (store in database, etc.)
    # Example:
    user_data = {
        'first_name' : first_name,
        'last_name' : last_name,
        'genre' : genre,
        'date_of_birth' : date,
        'marital_status' : Situation_Familiale,
        'weight' : poids,
        'taille' : taille,
        'email' : email,
        'password': password,
        'phone' : phone,
        'place' : place,
        'Country' : Country,

    }

    # Return a response (optional)
    return jsonify({'message': 'Registration successful', 'data': user_data})

@app.route('/demo', methods=['POST'])
def demo():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        name = request.form['name']
        mail_addr = request.form['mail']
        phone = request.form['phone']
        compte = request.form['compte']
        genre = request.form['Genre']
        activite = request.form['Activité']
        lieu = request.form['lieu'] 

        # Enregistrer les données dans Firebase Firestore
        doc_ref = db.collection('doctors').document()
        doc_ref.set({
            'name': name,
            'mail': mail_addr,  
            'phone': phone,
            'compte': compte,
            'genre': genre,
            'activite': activite,
            'lieu': lieu
        })
        return 'Data has been successfully submitted to Firebase!'
    else:
        return 'Invalid request method'

#-------Login Patient --------------------------------------------------------------

@app.route('/login_patient', methods=['POST'])
def login_patient():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        email = request.form['email']
        password = request.form['password']

        # Vérifier si les informations de connexion sont valides en interrogeant Firestore
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).where('password', '==', password).limit(1).get()

        if len(query) > 0:
            # Si les informations de connexion sont valides, rediriger vers la page d'accueil avec l'email comme paramètre
            return redirect(url_for('index', email=email))
        else:
            # Si les informations de connexion sont invalides, rediriger vers la page de connexion avec un message d'erreur
            return 'Identifiants invalides. Veuillez réessayer.'

    else:
        # Si la méthode de la requête n'est pas POST, renvoyer une erreur
        return 'Invalid request method'
@app.route('/')
def index():
    email = request.args.get('email')  # Récupère l'email depuis l'URL
    return render_template('index.html', email=email)

#-------Login Doctor------------------------------------------------------------

@app.route('/login_doctor', methods=['POST'])
def login_doctor():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        username = request.form['username']
        password = request.form['password']

        # Vérifier si les informations de connexion sont valides en interrogeant Firestore
        users_ref = db.collection('compte')
        query = users_ref.where('username', '==', username).where('password', '==', password).limit(1).get()

        if len(query) > 0:
            # Si les informations de connexion sont valides, enregistrer le nom d'utilisateur dans la session
            session['username'] = username
            # Rediriger vers la page pour ajouter un rendez-vous
            return redirect(url_for('add_time', username=username))
        else:
            # Si les informations de connexion sont invalides, rediriger vers la page de connexion avec un message d'erreur
            return 'Identifiants invalides. Veuillez réessayer.'

    else:
        # Si la méthode de la requête n'est pas POST, renvoyer une erreur
        return 'Invalid request method'
    

#--------- Add times -------------------------------------------------------
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        # Check if the user is logged in
        if 'username' in session:
            # Retrieve the data from the form
            date = request.form.get('date')
            time = request.form.get('time')
            username = session['username']  # Retrieve the username from the session

            # Get current date and time
            current_datetime = datetime.now()

            # Parse the selected date and time
            appointment_datetime = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')

            # Check if the selected date and time is in the future
            if appointment_datetime > current_datetime:
                # Generate a unique ID for the entry
                entry_id = str(uuid.uuid4())

                # Determine the amount based on the time
                appointment_time = appointment_datetime.time()
                if appointment_time >= datetime.strptime('18:00', '%H:%M').time() and appointment_time < datetime.strptime('23:00', '%H:%M').time():
                    amount = 3000
                elif appointment_time >= datetime.strptime('08:00', '%H:%M').time() and appointment_time < datetime.strptime('18:00', '%H:%M').time():
                    amount = 2000
                else:
                    amount = 6000  

                # Add data to Firestore database
                doc_ref = db.collection('dates').document(username).collection('add_time').document(entry_id)
                doc_ref.set({
                    'date': date,
                    'time': time,
                    'amount': amount
                })

                # Redirect to a confirmation or success page
                return redirect(url_for('add_time'))
            else:
                # If the selected date and time is in the past, return an error or redirect to an error page
                return 'Selected date and time must be in the future.'
        else:
            # If the user is not logged in, redirect to the login page
            return redirect(url_for('login'))
    else:
        # If the request method is not POST, return an error
        return 'Invalid request method'


#--------- Display times for dortors -------------------------------------------------------
@app.route('/rendez-vous')
def add_time():
    # Check if the user is logged in
    if 'username' in session:
        username = session['username']

        doc_ref = db.collection('dates').document(username).collection('add_time')

        # Fetch all documents from the 'add_time' collection
        docs = doc_ref.get()

        # Store dates and their corresponding unique times in a dictionary
        date_time_dict = {}

        # Get current date and time
        current_datetime = datetime.now()

        # Iterate over the documents and populate the dictionary
        for doc in docs:
            appointment_data = doc.to_dict()
            date = appointment_data['date']
            time = appointment_data['time']

            # Combine date and time into a datetime object
            appointment_datetime = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')

            # Check if the appointment is in the future
            if appointment_datetime > current_datetime:
                if date not in date_time_dict:
                    date_time_dict[date] = set()

                date_time_dict[date].add(time)

        # Prepare the data for rendering in the template
        data = [{'date': date, 'times': sorted(times)} for date, times in date_time_dict.items()]

        # Render the template with the formatted data
        return render_template('add_time.html', username=username, data=data)
    else:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('login'))

@app.route('/delete', methods=['POST'])
def delete_entry():
    if request.method == 'POST':
        # Retrieve the date and time from the AJAX request
        date = request.json['date']
        time = request.json['time']

        # Retrieve the username from the session
        username = session.get('username')

        if username:
            # Create a query to find the document to delete
            doc_ref = db.collection('dates').document(username).collection('add_time')
            query = doc_ref.where('date', '==', date).where('time', '==', time)

            # Execute the query
            docs = query.get()

            # Delete the documents found by the query
            for doc in docs:
                doc.reference.delete()

            # Redirect to the main page
            return redirect(url_for('add_time'))
        else:
            return redirect(url_for('login'))

@app.route('/rendez_vous')
def rendez_vous():
    # Retrieve doctor names from Firestore
    doctors_ref = db.collection('doctors').get()
    doctor_names = [doc.to_dict()['name'] for doc in doctors_ref]

    return render_template('Rendez-vous.html', doctor_names=doctor_names)


@app.route('/psy/<doctor>')
def psy(doctor):
    # Retrieve doctor details from Firestore
    doctor_ref = db.collection('doctors').where('name', '==', doctor).get()
    doctor_details = doctor_ref[0].to_dict() if doctor_ref else None

    # Retrieve appointments for the doctor from Firestore
    appointments_ref = db.collection('dates').document(doctor).collection('add_time').get()
    
    # Get current date and time
    current_datetime = datetime.now()

    # Define appointments_by_date as an empty dictionary
    appointments_by_date = {}

    # Group appointments by date
    for appointment in appointments_ref:
        appointment_data = appointment.to_dict()
        date = appointment_data['date']
        time = appointment_data['time']
        amount = appointment_data.get('amount')  # Fetch amount safely

        # Parse date and time strings into datetime objects for comparison
        appointment_datetime = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')

        # Check if appointment is in the future
        if appointment_datetime > current_datetime:
            if date not in appointments_by_date:
                appointments_by_date[date] = []

            # Append time and amount to the list of times for this date
            appointments_by_date[date].append({'time': time, 'amount': amount})

    # Prepare the data for rendering in the template
    data = [{'date': date, 'appointments': sorted(appointments, key=lambda x: x['time'])} for date, appointments in appointments_by_date.items()]

    return render_template('psy.html', doctor_details=doctor_details, data=data)


#----Chat--------------------------------------------------------------------------

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    user_message = data['message']
    
    # Get response from main.get_response function
    answer = get_response(user_message)
    
    return jsonify({'message': answer})

@app.route('/api/history', methods=['GET'])
def api_history():
    return jsonify(chat_history)

#-----------Page----------------------------------------------------------------------

@app.route('/404')
def error():
    return render_template('404.html')


@app.route('/blog')
def blog():
    return render_template('articl1.html')

@app.route('/blog2')
def blog2():
    return render_template('articl2.html')

@app.route('/blog3')
def blog3():
    return render_template('articl3.html')

@app.route('/blog4')
def blog4():
    return render_template('articl4.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio-details.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/sign')
def sign():
    return render_template('sign.html') 

@app.route('/service')
def service():
    return render_template('service.html')   

@app.route('/doctor')
def doctor():
    return render_template('psychiatre.html')

@app.route('/psychiatres')
def doc():
    # Retrieve doctor names from Firestore
    doctors_ref = db.collection('doctors').get()
    doctor_names = [doc.to_dict()['name'] for doc in doctors_ref]

    return render_template('doctor.html', doctor_names=doctor_names)

@app.route('/news')
def news():
    return render_template('news-single.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginPatient')
def loginPatient():
    return render_template('loginPatient.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/Payment')
def Payment():
    return render_template('Payment.html')


if __name__ == '__main__':
    app.run(debug=True)
