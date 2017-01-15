from django import template
from troca.models import Project, Skills_categories, Skills, UserProfile, Collaboration, CambioContrasena, Comment,Notification, UserFavsAndNotificarions
from django.contrib.contenttypes.models import ContentType
register = template.Library()

@register.simple_tag
def get_skill(user):
    userProfile = UserProfile.objects.get(user=user) 
    obj = user_profile.category.all()
    return obj


@register.filter(name='user_gives') # 0:no puede nada | 1:puede donar | 2:puede trocar
def is_user_gives_to_project(usu, project):	# Set(user_skills)   
	estado=0;
	cat=set({})
	if usu and project.user != usu.user:
		cat=set(project.category.all()) & set(usu.category.all())
		if len( cat)>0:
			estado=1;
			userProjects = Project.objects.all().filter(user=usu.user).filter(isActive=True)	# Proyectos del usuario
			needs_userProjects=set([]) # crea un set vacio para las necesidades del usuario
			for y in userProjects.all():
				needs_userProjects.update(y.category.all()) # agrega las necesidades nuevas al set
			autor_profile = UserProfile.objects.get(user=project.user)
			autor_skills = set(autor_profile.category.all()) # set de habilidades del autor del proyecto
			cat_rev=autor_skills&needs_userProjects
			if len( cat_rev)>0:
				estado=2      
	print(str(project)+"\n"+str(project.user)+"\n"+str(autor_profile)+"\n")
	return estado
 
@register.filter(name='trueques_no_leidos') 
def trueques_no_leidos(usu):	
	col = len(Collaboration.objects.all().filter(autor=usu).filter(visto=False))
	res=""
	if col>0:
		res="("+str(col)+")"
	return res

@register.filter(name='comentarios_no_leidos') 
def comentarios_no_leidos(usu):	
	col = len(Comment.objects.all().filter(userProject=usu).exclude(userComment=usu).filter(visto=False))
	res=""
	if col>0:
		res="("+str(col)+")"
	return res

@register.filter(name='get_responds') 
def get_responds(com):	
	return com.responds.all();

@register.filter(name='get_html_responds') 
def get_html_responds(pk):
	print(str(com));
	res= '<div class="respuesta">';
	res +='<div class="fotoComentario" style="display: inline-block; width:30px;">';
	res +='<a href="/perfil/'+str(com.userRespond.id)+'">';
	res +='<div class="img-container-user circular" style="background-image: url(\''+str(com.userProfileRespond.avatar_url.url_700x700)+'\');  width:30px;  height:30px;">';
	res +='</div>';
	res +='</a>';
	res +='</div>';
	res +='<div class="infoComentario" style="display: inline-block;">';
	res +='<h5 class="mb0"><a href="/perfil/'+str(com.userRespond.id)+'">'+str(com.userRespond.username)+'</a> </h5> ';
	res +='<p class="mb0 comentario">';
	res +='"'+str(com.respond)+'"';
	res +='</p>';
	res +='</div>';
	res +='</div>';
	return res;	
	
@register.filter(name='get_type') 
def get_type(name=''):
	res=contTypeComment = ContentType.objects.get(app_label='troca', model=name).id;
	return res;

@register.filter(name='cant_proyectos') # retorna la cantidad de proyectos de un usuario
def cant_proyectos(usu):		
	cat=set(Project.objects.all().filter(user=usu.user));
	cantidad=len(cat);	
	return cantidad;

@register.filter(name='cant_trueques') # retorna la cantidad de trueques de un usuario aceptados
def cant_trueques(usu):		
	cat_1=set(Collaboration.objects.all().filter(autor=usu.user).filter(isActive='1'));
	print(cat_1);
	cat_2=set(Collaboration.objects.all().filter(collaborator=usu.user).filter(isActive='1'));
	print(cat_2);
	cat=cat_1|cat_2;
	cantidad=len(cat);	
	return cantidad;

# @register.simple_tag
@register.filter(name='get_projects_favs') 
def get_projects_favs(user):
	fav=get_favs(user);
	pro=fav.fav_projects.all();
	return pro;
  
# @register.simple_tag
@register.filter(name='get_collas_favs') 
def get_collas_favs(user):
	fav=get_favs(user);
	coll=fav.fav_collabs.all();
	return coll;

@register.filter(name='get_count_notifications') 
def get_count_notifications(user,project):
	count=0;
	fav=get_favs(user);
	notis=set(fav.notifications.all().filter(projectNotification=project).filter(isActive__lte=0));
	if notis:
		count=len(notis);
	return count;

@register.filter(name='get_count_all_notifications') 
def get_count_all_notifications(user):
	count=0;
	fav=get_favs(user);
	notis=set(fav.notifications.all().filter(isActive__lte=0));
	if notis:
		count=len(notis);
	return count;

# crea un nuevo objeto UserFavsAndNotificarions si no hay uno esistente con el usuario requerido.
def get_favs(user):
	try: 
		favs= UserFavsAndNotificarions.objects.get(user=user)
	except UserFavsAndNotificarions.DoesNotExist:
		favs = UserFavsAndNotificarions(user=user);
		favs.save();
	return favs;

@register.assignment_tag
def get_user_profile(user):
	userProfile = UserProfile.objects.get(user=user) 
	return userProfile;
	

  
  