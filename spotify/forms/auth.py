

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,Length,EqualTo



# class RegisterForm(FlaskForm):
#
#     email=StringField('邮箱',validators=[DataRequired(),Email()])
#     password=PasswordField('密码',validators=[DataRequired(),Length(8,128),EqualTo('password2')])
#     password2=PasswordField('再次输入密码',validators=[DataRequired(),Length(8,128)])
#     name=StringField('昵称',validators=[DataRequired()])
#     weeixin=StringField('微信号',validators=[DataRequired()])
#     submit=SubmitField('提交')


class LoginForm(FlaskForm):
    username = StringField('管理员名称', validators=[DataRequired()])
    password = StringField('管理员密码', validators=[DataRequired()])
    rememberme=BooleanField('记住我')
    submit=SubmitField('登录')

# class ForgetForm(FlaskForm):
#     email=StringField('邮箱',validators=[DataRequired(),Email()])
#     submit=SubmitField()
#
#
# class ResetPasswordForm(FlaskForm):
#     email=StringField('邮箱',validators=[DataRequired(),Email()])
#     password=StringField('密码',validators=[DataRequired(),Length(8,128),EqualTo('password2')])
#     password2=StringField('检验密码',validators=[DataRequired(),Length(8,128)])
#     submit=SubmitField('提交')
