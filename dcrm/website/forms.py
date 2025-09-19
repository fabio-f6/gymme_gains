from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Exercise, Plan


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
    first_name = forms.CharField(label="", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(label="", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class AddExerciseForm(forms.ModelForm):
    exercise_name = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Exercise name", "class": "form-control"}), label="", max_length=50)
    exercise_description = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={"placeholder": "Exercise description", "class": "form-control", "rows": 3}), label="")
    exercise_sets = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Sets", "class": "form-control"}), label="", max_length=10)
    exercise_reps = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Reps", "class": "form-control"}), label="", max_length=10)
    exercise_weight = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Weight", "class": "form-control"}), label="", max_length=10)
    exercise_rest = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Rest", "class": "form-control"}), label="", max_length=10)

    class Meta:
        model = Exercise
        exclude = ('created_by',)


class AddPlanForm(forms.ModelForm):
    # só mostra os exercícios do usuário logado
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Plan
        fields = ["plan_name", "exercises"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["exercises"].queryset = Exercise.objects.filter(created_by=user)
