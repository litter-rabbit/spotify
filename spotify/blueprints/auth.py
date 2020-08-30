
from flask import Blueprint,render_template,redirect,url_for,flash
from spotify.forms.auth import LoginForm
from flask_login import login_user, current_user,login_required,logout_user
from spotify.models import Admin
auth_bp=Blueprint('auth',__name__)

@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        admin= Admin.query.filter_by(username=form.username.data).first()
        if form.username.data==admin.username and form.password.data==admin.passwrod:
            login_user(admin,form.rememberme)
            flash('登录成功')
            return redirect(url_for('main.index'))
        else:
            flash('用户名或者密码错误')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html',form=form)


@auth_bp.route('/logout')
@login_required
def logout():

    logout_user()
    flash('退出登录成功','success')

    return redirect(url_for('auth.login'))



