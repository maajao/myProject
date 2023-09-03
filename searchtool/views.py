from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Database, User
from .forms import UserForm, DatabaseForm, LoginForm

class DatabaseIndex(generic.ListView):

    template_name = "searchtool/database_index.html"

    def get_queryset(self):
        return Database.objects.all().order_by("-id")

class CurrentDatabase(generic.DeleteView):
    model = Database
    template_name = "searchtool/database_detail.html"

    def get(self, request, pk):
        try:
            database = self.get_object()
        except:
            return redirect("database_index")
        return render(request, self.template_name, {"database": database})

    def post(self, request, pk):
        if request.user.is_authenticated:
            if "edit" in request.POST:
                return redirect("edit_database", pk=self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, "Only admin can delete data.")
                    return redirect("database_index")
                else:
                    self.get_object().delete()
        return redirect("database_index")

class CreateDatabase(LoginRequiredMixin, generic.edit.CreateView):
    form_class = DatabaseForm
    template_name = "searchtool/create_database"

    def get(self,request):
        if not request.user.is_admin:
            messages.info(request, "Only admin has rights to add data.")
            return redirect("database_index")
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self,request): # metoda pro POST request, zkontroluje formular; pokud je validni, vytvori novy film; pokud ne, zobrazi formular s chybovou hlaskou
        if not request.user.is_admin:
            messages.info(request, "Only admin has rights to add data.")
            return redirect("database_index")
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("database_index")
        return render(request, self.template_name, {"form": form})

class UserViewRegister(generic.edit.CreateView):
    form_class = UserForm
    model = User
    template_name = "searchtool/user_form.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect("database_index")
        return render(request, self.template_name, {"form": form})

class UserViewLogin(generic.edit.CreateView):
    form_class = LoginForm
    template_name = "searchtool/user_form.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)

class UserViewRegister(generic.edit.CreateView):
    form_class = UserForm
    model = User
    template_name = "searchtool/user_form.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already login, therefore you can't register again.")
            return redirect("database_index")
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already login, therefore you can't register again.")
            return redirect("database_index")
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect("database_index")

        return render(request, self.template_name, {"form": form})

class UserViewLogin(generic.edit.CreateView):
    form_class = LoginForm
    template_name = "searchtool/user_form.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Already login. Can't login again.")
            return redirect("database_index")
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Already login. Can't login again.")
            return redirect("database_index")
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request,user)
                return redirect("database_index")
            else:
                messages.error(request, "This account does not exist.")
        return render(request, self.template_name, {"form": form})

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.info(request, "You can't logout if you are not login first.")
    return redirect("login")

class EditDatabase(LoginRequiredMixin, generic.edit.CreateView):
    form_class = DatabaseForm
    template_name = "searchtool/create_database.html"

    def get(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Only admin can amend data.")
            return redirect("database_index")
        try:
            film = Database.objects.get(pk=pk)
        except:
            messages.error(request, "Data does not exist.")
            return redirect("database_index")
        form = self.form_class(instance=film)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Only admin can amend data.")
            return redirect("database_index")
        form = self.form_class(request.POST)

        if form.is_valid():
            keyword = form.cleaned_data["keyword"]
            description = form.cleaned_data["description"]
            prob_quest = form.cleaned_data["prob_quest"]
            tags = form.cleaned_data["tags"]
            try:
                database = Database.objects.get(pk=pk)
            except:
                messages.error(request, "Data does not exist.")
                return redirect("database_index")
            database.keyword = keyword
            database.description = description
            database.prob_quest = prob_quest
            database.tags = tags
            database.save()
            return redirect("database_detail", pk=database.id)
        return render(request, self.template_name, {"form": form})