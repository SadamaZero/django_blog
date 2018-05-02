from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    user = auth.authenticate(username=username, password=password)

    # def clean_data(self):
    #     # cleaned_data = super(LoginForm, self).clean()
    #     # username = cleaned_data.get('username')
    #     # password = cleaned_data.get('password')
    #     username = self.cleaned_data['username']
    #     password = self.cleaned_data['password']
    #
    #     user = auth.authenticate(username=username, password=password)
    #     self.cleaned_data['user'] = user
    #     if user is None:
    #         raise forms.ValidationError('用户名或密码不正确')
    #
    #
    #     return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=30,
                               min_length=6,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': '请输入用户名'}
                               ))
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': '请输入邮箱号'}
                             ))
    password = forms.CharField(label='密码',
                               min_length=6,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': '请输入密码'}
                               ))
    password_check = forms.CharField(label='确认密码',
                                    min_length=6,
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'placeholder': '重复输入密码'}
                               ))

    def clean_username(self):
        # 是否被注册
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已被注册')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被注册')
        return email

    def clean_password_check(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        if password != password_check:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_check
