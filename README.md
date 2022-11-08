# QuotationPlatform-API
### How to run
#### install lib
```commandline
pip install -r  requirements.txt
```
init DB schema
```commandline
python manage.py makemigrations mapping_source 
python manage.py migrate 
```
Create admin user account
```commandline
python manage.py createsuperuser 
```
Run server
```commandline
python manage.py runserver  
```

admin page: [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
### API
#### GetPartMappingSource
![GetPartMappingSource](doc/image/GetPartMappingSource.png "GetPartMappingSource")
#### GetPartMappingSourceOCR
![GetPartMappingSourceOCR](doc/image/GetPartMappingSourceOCR.png "GetPartMappingSourceOCR")
#### PartMappingJson
![PartMappingJson](doc/image/PartMappingJson.png "PartMappingJson")
#### GetWinRate
![GetWinRate](doc/image/GetWinRate.png "GetWinRate")
#### CheckAlive
![CheckAlive](doc/image/CheckAlive.png "CheckAlive")