
from flask import Blueprint,jsonify,flash,redirect,url_for,request,render_template
from flask_login import login_required
from spotify.models import Order
from multiprocessing import Process
from spotify.extendtions import db
from spotify.parse import get


ajax_bp=Blueprint('ajax',__name__)


@ajax_bp.route('/parse/order',methods=['POST','GET'])

def new_order():

    email='qh0607284@163.com'
    password='07551012'
    link='https://www.spotify.com/us/family/join/invite/85yY34a95B6Ac99/'


    e=request.args.get('email')
    p=request.args.get('password')
    l=request.args.get('link')

    order = Order(email=e, password=p)
    db.session.add(order)
    t=Process(target=get,args=(e,p,l))
    t.start()
    flash('提交成功,正在处理','success')

    return redirect(url_for('main.index'))

@ajax_bp.route('/parse/orders',methods=['POST','GET'])
@login_required
def new_orders():


    orders=request.args.get('orders')

    infos=orders.split()
    l=int(len(infos))
    n=int(l/3)
    if l%3==0:
        for i in range(n):
            t=Process(target=get,args=(infos[i*3],infos[i*3+1],infos[i*3+2]))
            t.start()
        flash('提交完毕','success')
    else:
        flash('格式输入错误','danger')


    return redirect(url_for('main.index'))



@ajax_bp.route('/get/detail/<order_id>',methods=['POST','GET'])
@login_required
def get_detail(order_id):

    order=Order.query.filter_by(id=order_id).first()
    orders=Order.query.filter_by(email=order.email).all()
    buy_times=len(orders)
    return render_template('main/detail_poppu.html',order=order,buy_times=buy_times)

# @ajax_bp.route('/reorder',methods=['POST','GET'])
# @login_required

