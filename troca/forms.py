# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth.models import User
from models import Project, UserProfile, Skills, Skills_categories
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, MultiField, Field, HTML, Column, Div
from django.contrib.auth.forms import AuthenticationForm
from froala_editor.widgets import FroalaEditor



class SkillForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    title = forms.CharField(
        label = "Nombre de la habilidad",
        required = True,
    )

    description = forms.CharField(
        label = "Descripción",
        required = True,
        max_length = 140,
        widget = forms.Textarea
    )
    
    class Meta:
        model = Skills
        fields = ('title', 'category', 'description')

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

                Fieldset(
                    'Detalles de la habilidad',
                    'title',
                    'description',
                    css_class='large-6 medium-6 columns ml20'
                ),
                Fieldset(
                    'Categoria',
                    'category',
                    css_class='large-5 medium-5 columns'
                ),
                ButtonHolder(Submit('submit', 'Enviar', css_class='button radius expanded')),      

            )
    

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    helper = FormHelper()
    helper.form_tag = False

    username = forms.CharField(
        label = "Nombre de Usuario | minusculas",
        required = True,
    )

    first_name = forms.CharField(
        label = "Nombre",
        required = True,
    )

    last_name = forms.CharField(
        label = "Apellido",
        required = True,
    )

    email = forms.EmailField(
        label = "Correo electrónico",
        required = True,
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label = "Contraseña",
        required = True,
    )


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',  'email', 'password')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
              HTML("<div></div>"),
               HTML("<h3 class='custom-header'>Registrate en Troca</h3> <h4> Registrate, publica, colabora, crea.</h4>"),
              HTML("<div class='elemento_crear_proyecto'>"),
                'username',
              HTML("</div><div class='elemento_crear_proyecto'>"),
                'first_name', 
              HTML("</div><div class='elemento_crear_proyecto'>"),
                'last_name',
              HTML("</div><div class='elemento_crear_proyecto'>"),
                'email',
              HTML("</div><div class='elemento_crear_proyecto'>"),
                'password',
              HTML("</div><div class='elemento_crear_proyecto'>"),
                ButtonHolder(Submit('submit', 'Registrarse', css_class='button radius btn_crearProyecto'),  css_class=' text-center'),
              HTML("</div><div class='elemento_crear_proyecto'>"),
                Div(
                    HTML('<div class="elemento_crear_proyecto"> <label>¿Ya eres miembro? <br> <a class="enlace_rojo" href="/login/">Inicia sesion</a></label> <br>Conoce los <a href="#" class="enlace_negro">términos de servicio</a> </div>'),
                    css_class='field-bottom topborder padt15 text-center'
                ),
              HTML("</div>"),
                css_class='large-6 medium-8 medium-centered columns',
            ),
        )

class UserLoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput())
    helper = FormHelper()
    helper.form_tag = False

    username = forms.CharField(
        label = "Usuario",
        required = True,
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label = "Contraseña",
        required = True,
    )


    class Meta:
        model = User
        fields = ('username', 'password')
        
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
              HTML("<div></div>"),
               HTML("<h3 class='custom-header'>Iniciar sesión</h3> <h4>¡Que bueno tenerte de vuelta!</h4>"),
              HTML("<div class='elemento_crear_proyecto'>"),
                'username',
              HTML("</div><div class='elemento_crear_proyecto'>"),
                'password',
              HTML("</div><div class='elemento_crear_proyecto'>"),
              
                ButtonHolder(Submit('submit', 'Iniciar sesion', css_class='button radius btn_crearProyecto'), css_class=' text-center'),
                Div(
                    HTML('<p>Eres nuevo en Troca? <a href="/register/">Registrate</a> <br> Has olvidado tu contrasena? <a href="#" data-reveal-id="firstModal">Recuperar</a></p>'),
                    css_class='field-bottom topborder padt15 text-center'
                ),
                css_class='large-4 medium-4 large-centered medium-centered columns',
            ),
        )

        
class UserProfileForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    facebook = forms.CharField(
        label = "Facebook (Opcional)",
        required=False,
        widget=forms.URLInput
    )
    
    twitter = forms.CharField(
        label = "Twitter (Opcional)",
        required=False,
        #widget=forms.URLInput
    )
    
    avatar_url = forms.ImageField(
        label = "Cambiar Imagen",
        required = False,
        widget=forms.FileInput,
    )
       
    category = forms.ModelMultipleChoiceField(
        queryset = Skills.objects.all().order_by('title'), 
        widget = forms.SelectMultiple,
        label = "",
        required = True,
    )
    
    about = forms.CharField(
        label = "Cúentanos quíen eres :)",
        required = True,
        max_length = 140,
        widget = forms.Textarea
    )

    class Meta:
        model = UserProfile
        fields = ('category', 'about', 'avatar_url', 'facebook', 'twitter')
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'dropzone'
        self.helper.form_action ='#'
        self.helper.layout = Layout(
            Fieldset(
              "", 
              HTML("<div class='large-2 medium-2 columns elemento_crear_proyecto'> "),
              HTML("<img class='img-container-user-profile  circular' src= {% if user.userprofile.avatar_url %}'{{ user.userprofile.avatar_url.url_700x700 }}' {% else %} 'http://s22.postimg.org/sgwv8z7kx/url.jpg'{% endif %} style='width:100%;'> <div class='img_oculto'>"),
              'avatar_url',
              HTML("</div></div>"),
              Fieldset(
                "",
              HTML("<div class='elemento_crear_proyecto'>"),
              HTML("<h3 class='custom-header'>{{user.first_name}} {{user.last_name}}</h3>"),
              
              HTML("</div><div class='elemento_crear_proyecto'>"),
              'about',
              HTML("</div><div class='elemento_crear_proyecto red_social'>"),
              'facebook',
              HTML("</div><div class='elemento_crear_proyecto red_social'>"),
              'twitter',
              HTML("</div>"),
              css_class='large-5 medium-5 columns',
                ),
                Fieldset(
                  "",
                  HTML("<div class='elemento_crear_proyecto'>"),
                    'Habilidades',
                  HTML("</div><div class='elemento_crear_proyecto'>"),
                    'category',
                  HTML("</div>"),
#                     HTML("<a  href='/crea/habilidad/' target='_blank'><i class='fa fa-life-ring'></i> Falta alguna habilidad en el listado?</a>"),
                   ButtonHolder(Submit('submit', 'Guardar cambios', css_class='button radius btn_crearProyecto')),
                    css_class='large-5 medium-5 columns'
                ),
               
            )
        )
      

                                
class ProjectForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False    
    expire_date = forms.DateField(
        label = "Fecha de expiración",
        initial = "Seleccionar la fecha en que caduca el proyecto",
        required = True,
        
    )
    
    title = forms.CharField(
        label = "Título del proyecto",
        required = True,
        max_length = 80,
    )
    
    thumbnail_url = forms.ImageField(
#         label = "<span> <i class='fa fa-camera icon_subir_img'></i>Arrastrar la imagen aquí</span>",
      label = "<span> <i class='fa fa-camera icon_subir_img'></i>Presionar para subir imagen</span>",
        required = True,
      widget=forms.FileInput,
    )
    
    summary = forms.CharField(
        label = "Descripcion Corta",
        required = True,
        max_length = 140,
        widget = forms.Textarea
      
    )
    
    content = forms.CharField(
        label = "Detalles del proyecto",
        required = True,
        widget = FroalaEditor
    )
    needs = forms.CharField(
        label = "Añade información adicional sobre las necesidades del proyecto (Opcional)",
        required = False,
        widget = FroalaEditor
    )
    
    category = forms.ModelMultipleChoiceField(
        queryset = Skills.objects.all().order_by('title'), 
        widget = forms.SelectMultiple,
        label = "",
        required = True,
        
    )
    
    
    class Meta:
        model = Project
        fields = ('title','expire_date','content','category', 'summary', 'needs', 'thumbnail_url')
        
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'dropzone'
        self.helper.form_action ='#'
        self.helper.layout = Layout(                   
            Fieldset(
              Field('Informacion del proyecto'),
              HTML('<h3 class="custom-header">Información del proyecto</h3>'),
              HTML("<div class='elemento_crear_proyecto'>"),
              Field('title',css_class='titulo_crear_proyecto',placeholder="Título del proyecto"),
              HTML('</div> <div class="elemento_crear_proyecto subir_imagen"  style="background-image:url( \'{{object.thumbnail_url.url_700x700}}\'); background-size: cover;background-repeat: no-repeat;">'),
              Field('thumbnail_url',),
              HTML("</div><div class='elemento_crear_proyecto'>"),
              Field('summary', placeholder="Descripcion Corta"),
              HTML("</div><div class='elemento_crear_proyecto'>"),
              Field( 'content',css_class='info_proyecto'),    
              HTML("</div><div class='elemento_crear_proyecto'>"),
              Field(
                'expire_date',
              css_class='datepicker'
              ),
              HTML("</div>"),
              css_class='large-6 medium-6 columns'
            ),
          Fieldset(
                '',
                HTML("<div class='elemento_crear_proyecto'>"),
                'Necesidades',
                HTML("</div><div class='elemento_crear_proyecto'>"),
                'category',
                HTML("</div><div class='elemento_crear_proyecto'>"),
                'needs',
                HTML("</div><div class='elemento_crear_proyecto'>"),
                ButtonHolder(Submit('submit', 'Publicar', css_class='button radius btn_crearProyecto')),
                HTML("</div>"),
                css_class='large-6 medium-6 columns'
            ),
            
        )
    
    
class NewPasswordForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label = "Nueva Contraseña",
        required = True,
    )


    class Meta:
        model = User
        fields = ('password','password')

    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'password',
                ButtonHolder(Submit('submit', 'Aceptar', css_class='button radius'),  css_class=' text-center'),                    
                css_class='large-4 medium-4 medium-centered columns',
            ),                   
        )