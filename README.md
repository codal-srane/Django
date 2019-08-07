## A Practice Repository for the following:  
- Git Commands
- Django
- DRF  


### Git Tasks:  

1. Created a git repository.  
2. Added two scripts to the repository master viz. Hello.py (Prints 'Hello') and HelloLoop.py (Prints 'Hello' 5 times using a 'for' loop).  
3. Created a branch called 'loop-modify'.  
4. Modified HelloLoop.py script in the master (Changed 'for' loop to 'do-while' loop).  
5. Modified HelloLoop.py script on the 'loop-modify' branch (Changed 'for' loop to 'while' loop).  
6. Merged the branch with the master and resolved conflicts using the Terminal; 'do-while' loop was selected. Also tried the same by pushing the branch from local to repository and creating a pull request, and then resolving the conflicts using Github GUI.  
7. Pushed the changes from local to the repository.  


### Using nginx to make a project publicly available via a private ip address:  

1. Create a new folder 'Django_Test'  
2. Create a new virtual environment 'test_project'    
```
> virtualenv test_project  
```
3. Activate the virtual environment    
```
> cd test_project
> source bin/activate
```
4. Install Django, uWSGI and nginx (Assuming HomeBrew is already installed)    
```
> pip install django
> pip install uwsgi
> brew install nginx
```
5. Create a django project named 'test_project' and run it locally     
```
> django-admin startproject test_project
> cd test_project
> python manage.py runserver
```
The project starts running on the localhost.  

6. Run uWSGI for accessing Django site    
```
> uwsgi --http :8000 --module test_project.wsgi
```  
In some cases there might be a "ModuleNotFoundError: No module named 'django'" Error. To prevent this error, include the following line in the 'wsgi.py' file so that the site-packages folder path could be accessed where the django file resides.  
```
> sys.path.append('<PATH_TO_VIRTUALENV>/Lib/site-packages')
```  
7. Start nginx  
```
> brew services start nginx
```
nginx starts by default on port 8080. Can be accessed using 'http://localhost:8080' on the browser.  

8. Configure nginx for your site

Download [uwsgi_params file](https://github.com/nginx/nginx/blob/master/conf/uwsgi_params). Place it in the 'test_project' directory at location where manage.py file resides.  

Create a nginx configuration file 'test_project_nginx.conf' at the same location and add the following contents to it  
```
# the upstream component nginx needs to connect to
upstream django {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8001; # for a web port socket
}

# configuration of the server
server {
    # the port your site will be served on
    listen      8000;
    # the domain name it will serve for
    server_name 192.168.0.194; # substitute your machine's IP address or FQDN
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias /path/to/your/mysite/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /path/to/your/mysite/static; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /path/to/your/mysite/uwsgi_params; # the uwsgi_params file you installed
    }
}
```
Also add the server to the 'ALLOWED_HOSTS' list under settings.py file. Create a soft link to test_project_nginx.conf in /usr/local/etc/nginx/servers to make nginx find the configuration file and apply it.  
```
ln -sf /path/to/your/mysite_nginx.conf /usr/local/etc/nginx/servers
```
9.   Restart nginx and run uWSGI for the Django site  
```
> brew services restart nginx
> uwsgi --http :8001 --module test_project.wsgi
```
The Django site is now publicly available. You should be able to access the Django site using private ip 'http://192.168.0.194:8001' on your web browser.  

#### References  
- https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html  
- https://www.sean-lan.com/2016/09/15/django-uwsgi-nginx/  