from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import CustomUserCreationForm, CustomerForm, SellerForm

@login_required
def profileMenu(request):
    if request.user.is_seller:
        return redirect('dashboard')
    elif request.user.is_customer:
        return redirect('home')
    else:
        return render(request,'users/p_menu.html',{})


# Create your views here.
class customerProfileView(View,LoginRequiredMixin):
    def get(self, request):
        profile_form = CustomerForm

        context ={ 'profile_form' : profile_form }

        return render(request,'users/profile.html', context)
    
    def post(self,request):
        profile_form = CustomerForm(
            request.POST
        )

        if profile_form.is_valid():
            user = request.user
            user.is_customer = True
            user.save()
            profile = profile_form.save(commit=False)
            profile.cuser = user
            profile.save()

            return redirect('home')

        else:
            context = {
                'profile_form': profile_form
            }
            return render(request, 'users/profile.html', context)


class sellerProfileView(View,LoginRequiredMixin):
    def get(self, request):
        profile_form = SellerForm

        context ={ 'profile_form' : profile_form }

        return render(request,'users/profile.html', context)
    
    def post(self,request):
        profile_form = SellerForm(
            request.POST
        )

        if profile_form.is_valid():
            user = request.user
            user.is_seller = True
            user.save()
            profile = profile_form.save(commit=False)
            profile.cuser = user
            profile.save()

            return redirect('dashboard')

        else:
            context = {
                'profile_form': profile_form
            }
            return render(request, 'users/profile.html', context)

class customerRegisterView(View):
    def get(self, request):
        user_form = CustomUserCreationForm()
        profile_form = CustomerForm()
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        
        return render(request, 'users/register.html', context)
    
    def post(self,request):
        user_form = CustomUserCreationForm(
            request.POST 
        )
        profile_form = CustomerForm(
            request.POST
        )

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_customer = True
            user.save()
            profile = profile_form.save(commit=False)
            profile.cuser = user
            profile.save()

            return redirect('dashboard')

        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            return render(request, 'users/register.html', context)

class sellerRegisterView(View):
    def get(self, request):
        user_form = CustomUserCreationForm()
        profile_form = SellerForm()
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        
        return render(request, 'users/register.html', context)
    
    def post(self,request):
        user_form = CustomUserCreationForm(
            request.POST 
        )
        profile_form = SellerForm(
            request.POST
        )

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_seller = True
            user.save()
            profile = profile_form.save(commit=False)
            profile.cuser = user
            profile.save()
            return redirect('dashboard')


        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            return render(request, 'users/register.html', context)

