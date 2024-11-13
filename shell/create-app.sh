python manage.py startapp $1 --template=codebase/app_template
mkdir -p $1/templates/$1
mv $1 codebase/$1
