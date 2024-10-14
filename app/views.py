from django.shortcuts import render, redirect, reverse
from app.models import Blog, Comment
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def Homepage(request):
  all_products = ['tote bag', 'shoes', 'jewelries']
  context = {"product": all_products} 
  return render(request, 'app/index.html', context)
  
def About(request):
  return render(request, 'app/about.html')

def hello(request):
  return render(request, 'app/hello.html')

@login_required
def blogs(request):
  user = request.user
  my_blogs = Blog.objects.filter(owner = user).order_by('-created_at')
  other_blogs = Blog.objects.all().exclude(owner = user).order_by('-created_at')
  # all_blogs = Blog.objects.all().order_by("-created_at")[:10]
  context = {"my_blogs": my_blogs, "other_blogs": other_blogs}
  return render(request, 'app/blogs.html', context)  
@login_required
def read(request, id):
  single_blog=Blog.objects.filter(id=id).first()
  user = request.user
  if not single_blog:
    messages.error(request, "Invalid blogs")
    return redirect(blogs)
  blog_comments = Comment.objects.filter(blog = single_blog).order_by('-created_at')
  context={'blog': single_blog , 'comments': blog_comments}
  if request.method == "POST":
    body = request.POST.get('comment')
    if not body:
      messages.error(request, "comment can't be empty")
      return redirect(reverse("read", kwargs = {'id':id}))
    Comment.objects.create(
      owner = user,
      blog = single_blog,
      body = body
    )
    return redirect(reverse("read", kwargs = {'id':id}))
  return render(request, 'app/read.html', context)  
@login_required
def delete(request, id):
  user = request.user
  single_blog=Blog.objects.filter(id=id).first()
  if not single_blog:
    messages.error(request, "Invalid blogs") 
    return redirect(blogs)
  if single_blog.owner != user:
    messages.error(request, "unauthorized access")  
    return redirect(blogs)
  single_blog.delete()
  messages.success(request, "Blog delete successfully")
  return redirect(blogs)
@login_required
def create(request):
  user = request.user
  if request.method == "POST":
    title = request.POST.get("title")
    body = request.POST.get("body")
    image = request.FILES.get('image')
    dsc = request.POST.get('description')
    if not title:
      messages.error(request, "Title is required")
      return redirect(create)
    if not body:
      messages.error(request, "body is required")
      return redirect(create)
    if not image:
      messages.error(request, "image is required")
      return redirect(create)

    # if not title or not body or not image:
    #   messages.error(request, "required")
    #   return redirect(create)
      if len(title) > 250:
        messages.error(request, "title is too long")
        return redirect(create)
    Blog.objects.create(
      title = title,
      body = body,
      image = image,
      description = dsc,
      owner=user
    )
    messages.success(request, "Blog created successfully")
    return redirect(blogs)
  return render(request, 'app/new.html')

@login_required
def edit(request, id):
  user = request.user
  single_blog = Blog.objects.filter(id=id).first()
  if not single_blog:
    messages.error(request, "Invalid blogs") 
    return redirect(blogs)
  if single_blog.owner != user:
    messages.error(request, "unauthorized access")
    return redirect(blogs)
  context = {"blog": single_blog}
  if request.method == "POST":
      title = request.POST.get("title")
      body = request.POST.get("body")
      image = request.POST.get("image")
      if not title or not body:
        messages.error(request, "blog unsuccessful")
        return redirect(blogs)
      single_blog.title = title
      single_blog.body = body
      if image:
        single_blog.image = image
      single_blog.save()
      messages.success(request, "blog saved successfully")
      return redirect(blogs)
  return render(request, "app/edit.html", context)

def signup(request):
  if request.user.is_authenticated:
    return redirect(Homepage)
  if request.method == "POST":
    username = request. POST.get("username")
    email = request. POST.get("email")
    firstname = request. POST.get("firstname")
    lastname = request. POST.get("lastname")
    password = request. POST.get("password")
    cpassword = request. POST.get("cpassword")

    if not username or not email or not password:
      messages.error(request, "all field required")
      return redirect(signup)
    if password != (cpassword):
      messages.error(request, "password required")
      return redirect(signup)
    if len(password) <8:
      messages.error(request, "password required")
      return redirect(signup)
    if len(password) <5:
      messages.error(request, "password required")
      return redirect(signup) 
    username_exists = User.objects.filter(username = username).exists()
    if username_exists:
      messages.error(request, "user already exist")
      return redirect (signup)
    email_exists = User.objects.filter(email = email).exists()
    if email_exists:
      messages.error(request, "email already exist")
      return redirect (signup)
    user = User.objects.create(
      username = username,
      email = email,
      first_name = firstname,
      last_name = lastname
    )
    user.set_password(password)
    user.save()
    messages.success(request,"signup succussful")
    return redirect(blogs)

  return render(request,"app/signup.html")

def login(request):
  if request.user.is_authenticated:
    return redirect(Homepage)
  next = request.GET.get("next")  
  if request.method == "POST":
    username = request.POST.get("username")
    password = request.POST.get("password")
    if not username or not password:
        messages.error(request, "all field required")
        return redirect(login)
    user = auth.authenticate(username = username, password = password)  
    if not user:
        messages.error(request, "invalid login")
        return redirect(login)
    auth.login(request, user)
    return redirect(next or Homepage)
  return render(request,"app/login.html")

def logout(request):
  auth.logout(request)
  return redirect(login)
