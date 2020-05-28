# Caboolture Gliding Club Website
This is a django web app which allows the Caboolture Gliding Club to query their SQL db of their daily flights through a browser. It allows queries/edits to the db using a web API which takes JSON objects. The web page includes responsive graphs created using highcharts.

This was built to run on a pythonanywhere instance using django 2.2.7. This upload only includes files I created/edited and none of the Django generated files as git cannot upload empty files, which the Django generated files included.

This was my first web python project and although it works well some of the code is fairly ugly. Some examples:
  - Some nearly copy-pasted code in catalog/forms.py
  - Model functions in views.py as the model was auto-generated then edited to match a legacy db and I was unsure what could be included       in models.py without breaking that
  - A general lack of comments
