# Import
from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DBNAME.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(1000),nullable=False)

    def __repr__(self):
        return f'<User {self.id}>'
    
# İçerik sayfasını çalıştırma
@app.route('/')
def index():
    Feedback = feedback.query.order_by(feedback.id).all()
    return render_template('index.html',Feedback=Feedback)


# Dinamik beceriler
@app.route('/', methods=['POST'])
def process_form():
    button_python = request.form.get('button_python')
    button_discord = request.form.get('button_discord')
    button_html = request.form.get('button_html')
    button_db = request.form.get('button_db')
    return render_template('index.html',
                           button_python=button_python,
                           button_discord=button_discord,
                           button_html=button_html,
                           button_db=button_db,) 

@app.route('/form_input', methods=['GET','POST'])
def form_input():
    if request.method == 'POST':
        email =  request.form['email']
        text =  request.form['text']

        # Veri tabanına gönderilecek bir nesne oluşturma
        Feedback = Feedback(email=email, text=text)

        db.session.add(Feedback)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
