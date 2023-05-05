from django.shortcuts import render,redirect
from socialapp.forms import LoginForm,RegistrationForm,PostForm
from django.contrib.auth.models import User
from django.views.generic import View,CreateView,FormView,TemplateView,ListView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from socialapp.models import Posts,Comments,UserProfile
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

# Create your views here.


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"you are not permitted to perform this action")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,never_cache]
class SignupView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name="registration.html"
    success_url=reverse_lazy("signin")

class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"

    def post(self,request,*args, **kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                print("success")
                return redirect("home")
            else:
                messages.error(request,"the username or password you entered is invalid. please try again")
                return render(request,self.template_name,{"form":form})

@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    model=Posts
    success_url=reverse_lazy("home")
    context_object_name="posts"

    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Posts.objects.all().exclude(user=self.request.user)

# loocalhost:8000/posts/1/
def add_comment(request,*args, **kwargs):
    post_id=kwargs.get("id")
    pos=Posts.objects.get(id=post_id)
    comm=request.POST.get("comment")
    pos.comments_set.create(comment=comm,user=request.user)
    return redirect("home")

def like_cmt(request,*args, **kwargs):
    cmt_id=kwargs.get("id")
    comm=Comments.objects.get(id=cmt_id)
    comm.like.add(request.user)
    comm.save()
    return redirect("home")


def post_likes(request,*args,**kwargs):
    pst_id=kwargs.get("id")
    pst=Posts.objects.get(id=pst_id)
    pst.likes.add(request.user)
    pst.save()
    messages.success(request,"you liked the post")
    return redirect("home")

@method_decorator(decs,name="dispatch")
class MyPostsView(ListView):
    model=Posts
    context_object_name="posts"
    template_name="myposts.html"

    def get_queryset(self):
        return Posts.objects.filter(user=self.request.user)

def sign_out(request,*args,**kwargs):
    logout(request)
    messages.success(request,"logout successfully")
    return redirect("signin")

def post_delete(request,*args,**kwargs):
    pst_id=kwargs.get("id")
    Posts.objects.filter(id=pst_id).delete()
    messages.success(request,"Post deleted succefully")
    return redirect("myposts")




class UserProfileView(CreateView):
    model=UserProfile
    context_object_name="userprof"
    Template_name="user.html"
    success_url=reverse_lazy("home")
    


