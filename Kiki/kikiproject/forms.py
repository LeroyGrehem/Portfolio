from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Project, UserProfile

# Forms creation

class ProjectForm(forms.ModelForm):
    name_project = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'input',
                                                                                'placeholder': 'Project Name: '}))
    description = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'input',
                                                                                'placeholder': 'Project Description: '}))
    git_link = forms.CharField(required=False, max_length=200, widget=forms.TextInput(attrs={'class': 'input',
                                                                                             'placeholder': 'GitHub link: '}))
    project_image = forms.ImageField(label="Project Image")

    class Meta:
        model = Project
        fields = ('name_project', 'description', 'git_link', 'project_image', 'tags')
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', True)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = required


class Profile(forms.ModelForm):
    profile_bio = forms.CharField(max_length=150, widget=forms.Textarea(attrs={'class': 'input',
                                                                               'placeholder': 'Personal Bio:'}))
    git_link = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'input',
                                                                             'placeholder': 'GitHab link'}))
    linledin_link = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'input',
                                                                                  'placeholder': 'LinkedIn:'}))
    profile_image = forms.ImageField(required=True)

    class Meta:
        model = UserProfile
        fields = ('profile_bio', 'git_link', 'linledin_link', 'profile_image')

    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', True)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = required



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'class': 'input',
                                                                          'placeholder': 'Email: '}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input',
                                                                                               'placeholder': 'First Name:'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input',
                                                                                              'placeholder': 'Last Name:'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', True)
        super(SignUpForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = required

        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''

        self.fields['password1'].widget.attrs['class'] = 'input'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''

        self.fields['password2'].widget.attrs['class'] = 'input'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''


class UpdateForm(UserChangeForm):
    email = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'class': 'input',
                                                                          'placeholder': 'Email: '}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input',
                                                                               'placeholder': 'First Name:'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input',
                                                                              'placeholder': 'Last Name:'}))


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', True)
        super(UpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = required

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username