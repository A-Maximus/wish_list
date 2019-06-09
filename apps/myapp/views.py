from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
# Item.objects.all().delete()

def index(request):
    return render(request, "index.html")


def create_user(request):
    print(request.POST)
    errors = User.objects.Reg_validator(request.POST)
    print(errors)
    if errors:
        for key, value in errors.items():
            messages.add_message(request, messages.ERROR, value, key)
        return redirect("/")
    else:
        password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=password_hash.decode())
        request.session['id'] = user.id
        return redirect("/dashboard")


# def wish_list(request, item_id):
#     context = {
#         "trip": Trip.objects.get(id=trip_id),
#         "users_joining_the_trip": Join.objects.filter(trip_id=trip_id)
#     }
#     return render(request, 'destination.html', context)


def dashboard(request):
    if 'id' in request.session:
        print("Logged In")
        print(request.session['id'])
        user = User.objects.get(id=request.session['id'])
        items = Item.objects.all()
        joins = Join.objects.filter(user_id=request.session['id'])
        my_wish_list = []
        other_wish_items = []

        for join in joins:
            my_wish_list.append(join.item_id)
        print(my_wish_list)
        for item in items:
            if item.id not in my_wish_list:
                other_wish_items.append(item)
            print(other_wish_items)
        context = {
            "user": user,
            "items": items,
            "joins": joins,
            "other_wish_items": other_wish_items
        }
        return render(request, 'dashboard.html', context)
    else:
        print(request.session['id'])
        return redirect("/")


def create_item(request):
    errors = Item.objects.Item_validator(request.POST)
    print(errors)
    if errors:
        for key, value in errors.items():
            messages.add_message(request, messages.ERROR, value, key)
        return redirect("/newitem")
    else:
        # print(request.POST['item'])
        # print(request.POST['wish_list_items'])
        item = Item.objects.create(item=request.POST['item'], added_by=User.objects.get(id=request.session['id']))
        # user = User.objects.get(id=request.session['id'])
        Join.objects.create(item=item, user_id=request.session['id'])
        return redirect("/dashboard")

def newitem(request):
    if request.session['id'] == 0:
        return redirect("/")
    return render(request, 'newitem.html')

def wishlistitems(request, item_id):
    context = {
        "item": Item.objects.get(id=item_id),
        "other_users_wish_list_items": Join.objects.filter(item_id=item_id)
    }
    return render(request, 'wishlistitems.html', context)

def login(request):
    errors = User.objects.Login_validator(request.POST)
    print("errors:", errors)
    if len(errors):
        for key, value in errors.items():
            messages.add_message(request, messages.ERROR, value, key)
        return redirect("/")
    else:
        users = User.objects.filter(username=request.POST["username"])
        print("users:", users)
        request.session['id'] = users[0].id
        print("logged in")
    return redirect("/dashboard")


def addtowishlist(request, item_id):
    Join.objects.create(item_id=item_id, user_id=request.session['id'])
    return redirect("/dashboard")


def removefromwishlist(request, item_id):
    Join.objects.get(item_id=item_id, user_id=request.session['id']).delete()
    return redirect("/dashboard")


def deleteitem(request, item_id):
    Item.objects.get(id=item_id).delete()
    return redirect("/dashboard")

def logout(request):
    request.session.clear()
    print("logged out")
    return redirect("/")
