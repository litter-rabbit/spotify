


from flask import Blueprint,render_template,request,current_app
from flask_login import login_required

from spotify.models import Order,Link



main_bp=Blueprint('main',__name__)

@main_bp.route('/',methods=['GET','POST'])
@login_required
def index():
    #
    per_page=current_app.config['PER_PAGE']
    page=request.args.get('page',1)
    page=int(page)
    pagination=Order.query.order_by(Order.timestamp.desc()).paginate(page,per_page)
    orders=pagination.items
    return render_template('main/index.html',orders=orders,page=page,pagination=pagination)


@main_bp.route('/links',methods=['GET','POST'])
@login_required
def links():
    #
    per_page=current_app.config['PER_PAGE']
    page=request.args.get('page',1)
    page=int(page)
    pagination=Link.query.order_by(Link.timestamp.desc()).paginate(page,per_page)
    links=pagination.items
    return render_template('main/links.html',links=links,page=page,pagination=pagination)


