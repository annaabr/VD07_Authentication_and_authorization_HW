from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, DeleteForm, ChangeEmailForm, ChangePasswordForm, ChangeUserForm

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Введены неверные данные')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/change', methods=['GET', 'POST'])
@login_required
def change():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль был изменен', 'success')
        return redirect(url_for('login'))
    return render_template('change.html', form=form, title='Change Password')

@app.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        user.email = form.email.dat
        db.session.commit()
        flash('Ваш E-mail был изменен', 'success')
        return redirect(url_for('login'))
    return render_template('change_email.html', form=form, title='Change Email')

@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(current_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('delete.html', form=form, title='Delete Account')


@app.route('/change_name', methods=['GET', 'POST'])
@login_required
def change_name():
    form = ChangeUserForm()
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        user.username = form.username.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('change_name.html', form=form, title='Change Name')