from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import google.generativeai as gen_ai
from PIL import Image
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Tree

# Configure Flask app and Gemini API
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecoscan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize database
db.init_app(app)

# Configure Gemini API
gen_ai.configure(api_key="")
gemini = gen_ai.GenerativeModel("gemini-1.5-flash")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def upload_image_to_gemini(image_path):
    uploaded_file = gen_ai.upload_file(path=image_path, display_name=os.path.basename(image_path))
    return uploaded_file

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('signup'))
            
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('dashboard'))
        
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing'))

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        
        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            gemini_file = upload_image_to_gemini(filepath)
            description_response = gemini.generate_content([gemini_file, "Provide tips on how to recycle the item in the image. Keep conversation to that context itself."])
            description_text = description_response.text

            session['image_path'] = filepath
            session['description'] = description_text
            session['chat_history'] = [{"sender": "Gemini", "message": description_text}]

            return redirect(url_for('chat'))

    return render_template('index.html')

@app.route('/plant-tree', methods=['GET', 'POST'])
@login_required
def plant_tree():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        
        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                gemini_file = upload_image_to_gemini(filepath)
                verification_response = gemini.generate_content([
                    gemini_file, 
                    """Analyze this image and determine if it shows a newly planted tree or plant. 
                    Consider: fresh soil, planting context, young plant/tree.
                    Respond in this format:
                    TYPE: TREE/PLANT/NO
                    REASON: Brief explanation
                    """
                ])
                
                response_text = verification_response.text
                
                # Extract the type from response
                if 'TYPE: TREE' in response_text.upper():
                    result = 'TREE'
                elif 'TYPE: PLANT' in response_text.upper():
                    result = 'PLANT'
                else:
                    result = 'NO'
                
                if result in ['TREE', 'PLANT']:
                    rewards = 3 if result == 'TREE' else 1
                    
                    new_tree = Tree(
                        image_path=filepath,
                        rewards_earned=rewards,
                        user_id=current_user.id,
                        gemini_response=response_text
                    )
                    
                    current_user.total_rewards += rewards
                    db.session.add(new_tree)
                    db.session.commit()
                    
                    return jsonify({
                        'success': True,
                        'message': f'Congratulations! You earned {rewards} rewards for your {result.lower()}!',
                        'redirect': url_for('dashboard')
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': 'The image does not appear to show a newly planted tree or plant. Please upload a valid image.',
                        'redirect': None
                    })
                    
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': 'An error occurred while processing your image. Please try again.',
                    'redirect': None
                })

    return render_template('plant_tree.html')

@app.route('/dashboard')
@login_required
def dashboard():
    trees = Tree.query.filter_by(user_id=current_user.id).order_by(Tree.planted_at.desc()).all()
    return render_template('dashboard.html', trees=trees)

@app.route('/delete-tree/<int:tree_id>', methods=['POST'])
@login_required
def delete_tree(tree_id):
    tree = Tree.query.filter_by(id=tree_id, user_id=current_user.id).first()
    
    if tree:
        try:
            # Reduce user's rewards
            current_user.total_rewards -= tree.rewards_earned
            
            # Delete the tree's image file if it exists
            if os.path.exists(tree.image_path):
                os.remove(tree.image_path)
            
            # Delete the tree record
            db.session.delete(tree)
            db.session.commit()
            
            # Get updated tree count
            remaining_trees = Tree.query.filter_by(user_id=current_user.id).count()
            
            return jsonify({
                'success': True,
                'message': 'Tree removed successfully',
                'new_total': current_user.total_rewards,
                'remaining_trees': remaining_trees
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': 'Error removing tree'
            }), 500
    
    return jsonify({
        'success': False,
        'message': 'Tree not found'
    }), 404

@app.route('/chat')
def chat():
    image_path = session.get('image_path', None)
    chat_history = session.get('chat_history', [])
    return render_template('chat.html', image_path=image_path, chat_history=chat_history)

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form.get('question')
    image_path = session.get('image_path', None)

    gemini_file = upload_image_to_gemini(image_path)

    session['chat_history'].append({"sender": "System", "message": "Gemini is thinking..."})

    gemini_response = gemini.generate_content([gemini_file, user_question])
    response_text = gemini_response.text

    session['chat_history'].pop()
    session['chat_history'].append({"sender": "User", "message": user_question})
    session['chat_history'].append({"sender": "Gemini", "message": response_text})

    return jsonify({"response": response_text, "chat_history": session['chat_history']})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
