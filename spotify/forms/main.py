
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,TextAreaField
from wtforms.validators import Optional,DataRequired,Email,Length



class OrderForm(FlaskForm):
    email=StringField('账号',validators=[DataRequired()])
    password=StringField('密码',validators=[DataRequired()])
    submit=SubmitField('提交')


# class LoginForm(FlaskForm):
#     username=StringField('管理员名称',validators=[DataRequired()])
#     password=StringField('管理员密码',validators=[DataRequired()])

# class PlayerForm(FlaskForm):
#     name=StringField('球员名称',validators=[DataRequired()])
#     rank=SelectField('球员等级',coerce = int,choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10')])
#     area=SelectField('球员大区',coerce = int,choices=[(1,'华东电信'),(2,'华南电信'),(3,'西南电信'),(4,'华北联通')])
#     is_buy=SelectField('出售或收购',coerce= int,choices=[(1,'出售'),(2,'收购')])
#     backup=StringField('备注',validators=[Optional(),Length(1,10)])
#     submit=SubmitField('提交')
#
#
#
# class AdviceForm(FlaskForm):
#     body=TextAreaField('建议内容',validators=[DataRequired()])
#     email=StringField('联系邮箱',validators=[Optional(),Email()])
#     submit=SubmitField('提交')
