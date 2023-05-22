from django.shortcuts import redirect, render
from django.views import View

from silk_road.accounts.forms import CustomUserCreationForm, CustomerForm, SellerForm

# Create your views here.

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

