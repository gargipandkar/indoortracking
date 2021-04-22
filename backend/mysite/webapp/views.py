from webapp.decorators import unauthenticated_user
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# For User auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import admin_only, unauthenticated_user, allowed_users, admin_only

from django.views.generic import ListView, CreateView
from .models import Floorplan, MappedPoint
from .forms import FloorplanForm, CreateUserForm

from django.urls import reverse_lazy
import json

# My python files
from tools import *
# import knnalgo
import extratrees
import randomforest
import saecnn
import evaldl
import evalreg

PROJECT_PHASE = "dev"
CURRENT_PLAN = ""


# User registration
def RegisterPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='user')
            user.groups.add(group)

            messages.success(request, "Account created for " + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)

# User login


@unauthenticated_user
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def LogoutUser(request):
    logout(request)
    return redirect('login')

# Webapp views


class HomePageView(ListView):
    model = Floorplan
    template_name = 'home.html'


class AddPlanView(CreateView):
    model = Floorplan
    form_class = FloorplanForm
    template_name = 'addplan.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        return super().form_valid(form)


# Communicate with Android app
def LoginMobileUser(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse("LOGIN_SUCCESS")
        else:
            return HttpResponse("LOGIN_FAILURE")

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'user'])


def GetAllPlans(request):
    if request.method == 'GET':
        plans = Floorplan.objects.all().values()
        plans_list = list(plans)
        return JsonResponse(plans_list, safe=False)
    if request.method == 'POST':
        global CURRENT_PLAN
        CURRENT_PLAN = request.POST.get("plan")
        print(CURRENT_PLAN)
        set_current_plan(CURRENT_PLAN)
        return HttpResponse(CURRENT_PLAN)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'user'])


def SaveMappedPoints(request):
    global CURRENT_PLAN
    if request.method == 'POST':
        mydata = json.loads(request.body.decode("utf-8"))
        print("Current plan = ", CURRENT_PLAN)

        for item in mydata:
            print("Point = ", item['point'])
            print("Vector = ", item['vector'])
            point = MappedPoint.objects.create(
                imgcoordinate=item['point'], scanvalues=item['vector'], plan=CURRENT_PLAN)

        # if PROJECT_PHASE == "dev":
        #     algols = [knnalgo.train_model,
        #               extratrees.train_model, randomforest.train_model]
        #     for algo in algols:
        #         istrained = algo(mydata)
        # else:
        #     istrained = knnalgo.train_model(mydata)
        
        istrained = knnalgo.train_model(mydata)

        if PROJECT_PHASE == "dev":
            # initialize excel file for model evaluation
            initialize_predfile()

        # update status of floorplan
        planobj = Floorplan.objects.get(title=CURRENT_PLAN)
        planobj.status = "MAPPED"
        planobj.save()

        print("Model Trained = ", istrained)
        return JsonResponse(list(["SAVED"]), safe=False)


# define counter variable for test points
TEST_POINT_COUNT = 0
TEST_POINT_MAX = get_test_count()

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'user'])


def GetLocation(request):
    global CURRENT_PLAN
    print("Current plan = ", CURRENT_PLAN)

    global TEST_POINT_COUNT
    global TEST_POINT_MAX

    # quick fix
    mydata = []
    rssistrls = list(MappedPoint.objects.all().filter(plan=CURRENT_PLAN))
    for item in rssistrls:
        tempdict = {}
        tempdict['point'] = item.imgcoordinate
        tempdict['vector'] = item.scanvalues
        mydata.append(tempdict)
    print(mydata)

    if PROJECT_PHASE == "dev" and TEST_POINT_COUNT == 0:
        algols = [knnalgo.train_model,
                  extratrees.train_model, randomforest.train_model]
        for algo in algols:
            istrained = algo(mydata)

    # update status of floorplan
        planobj = Floorplan.objects.get(title=CURRENT_PLAN)
        planobj.status = "MAPPED"
        planobj.save()

    # actual function
    mydata = json.loads(request.body.decode("utf-8"))
    testvector = mydata[0]['vector']
    print(testvector)

    if PROJECT_PHASE == "dev" and TEST_POINT_COUNT < TEST_POINT_MAX:
        print("# of test points = ", TEST_POINT_MAX)
        algols = [knnalgo.get_prediction,
                  extratrees.get_prediction, randomforest.get_prediction]
        ls = []
        for algo in algols:
            loc = algo(testvector)
            ls.append(loc.tolist())
        save_predictions(TEST_POINT_COUNT, ls)
        TEST_POINT_COUNT += 1

        print("Test point saved: ", TEST_POINT_COUNT)

    if TEST_POINT_COUNT == TEST_POINT_MAX:
        # evaluate_models()
        pass

    location = randomforest.get_prediction(testvector)
    print(location)
    locationls = location.tolist()
    # response format looks like --> [[0, 0]]
    return JsonResponse(list(locationls), safe=False)


# ONLY USED TO COMPARE MODEL PERFORMANCE
def EvaluateAlgos(request):
    plan_name = "SUTD CC Vertical"
    set_current_plan(plan_name)
    
    # # remove any unwanted APs if saved
    # planobj = Floorplan.objects.get(title=plan_name)
    # ls = planobj.aplist
    # ls = ls.replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
    # ls = ls.split(",")
    # cleanls = [item for item in ls if "SUTD_Wifi" in item or "SUTD_Guest" in item or "eduroam" in item]
    # print("Cleaned AP list: ", cleanls, " of length ", len(cleanls))
    # planobj.aplist = cleanls
    # planobj.save()
    
    # retrieve all data and convert to list of dictionaries
    mydata = []
    rssistrls = list(MappedPoint.objects.all().filter(plan=plan_name))
    for item in rssistrls:
        tempdict = {}
        tempdict['point'] = item.imgcoordinate
        tempdict['vector'] = item.scanvalues
        mydata.append(tempdict)

    # get model input
    x, y = get_model_inputs(mydata)
    print("Data points collected: ", len(x))
    print("# of APs: ", len(x[0]))
    # save as dataframe
    point_count = len(x)
    df = pd.DataFrame(data=x)
    df['target'] = y

    filename = "webapp/algos/" +plan_name.replace(" ", "") + "_data.xlsx"
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name='data', index=False)
        
    evalfile = "webapp/algos/" + plan_name.replace(" ", "") + "_evaluation.xlsx"

    # evaluate on all available models
    resls = []
    evalfunc=[evalreg.get_evaluation_results, evaldl.get_evaluation_results, saecnn.get_evaluation_results]
    for algoeval in evalfunc:
        ls = algoeval(x, y)
        resls+=ls
        
    resdf  = pd.DataFrame(resls)
    resdf.rename(columns={0: "Algo", 1: "Metric (MSE)", 2:"Euclidean distance"}, inplace = True)
    with pd.ExcelWriter(evalfile) as writer:
        resdf.to_excel(writer, sheet_name='evaluation', index=False)

    return HttpResponse(plan_name)
