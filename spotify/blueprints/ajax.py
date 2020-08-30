
from flask import Blueprint,flash,redirect,url_for,request,render_template
from flask_login import login_required
from spotify.models import Order,Link
from multiprocessing import Process
import _thread
from spotify.extendtions import db
from spotify.parse import get


ajax_bp=Blueprint('ajax',__name__)


@ajax_bp.route('/parse/order',methods=['POST','GET'])
@login_required
def new_order():

    e=request.args.get('email')
    p=request.args.get('password')

    while True:
        link=Link.query.first()
        if not link:
            flash('当前没有可用链接，请添加','danger')
            return redirect(url_for('main.links'))
        if link.times>0:
            break
        else:
            db.session.delete(link)
            db.session.commit()

    t=Process(target=get,args=(e,p,link))
    t.start()
    # _thread.start_new_thread(get,(e,p,link,))

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

@ajax_bp.route('/new/links',methods=['POST','GET'])
@login_required
def new_links():

    links=request.args.get('links')
    infos=links.split()
    for i in infos:
        link=Link(infos=i)
        db.session.add(link)
    db.session.commit()

    return redirect(url_for('main.links'))



@ajax_bp.route('/get/detail/<order_id>',methods=['POST','GET'])
@login_required
def get_detail(order_id):

    order=Order.query.filter_by(id=order_id).first()
    orders=Order.query.filter_by(email=order.email).all()
    buy_times=len(orders)
    return render_template('main/detail_poppu.html',order=order,buy_times=buy_times)


@ajax_bp.route('/delete/link/<link_id>',methods=['POST','GET'])
@login_required
def delete_link(link_id):
    link=Link.query.get(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('删除成功','success')
    return redirect(url_for('main.links'))


# @ajax_bp.route('/reorder',methods=['POST','GET'])
# @login_required

