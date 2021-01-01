# Project Title

Multi-Vendor Django E-Commerce Website with Stripe Support.

## Description

An e-commerce website built using the Django Framework. The website has vendor and customer user profile types with the ability to extend to other profile types; different permissions are set based on the profile type. Moreover, the website has a cart app that works using session variables. Also, there is the app of an order that uses Stripe for processing payments. The website templates were built by customizing free HTML templates from @neha, using Django template language. Tests are only set up for the users' app and checked using the coverage package.


## C4 Model Design Diagram

![marketplace](https://github.com/MohAyman3600/Multi-Vendor-Django-E-Commerce/blob/master/C4_model_arch/structurizr-59568-Marketplace.png)

![project-apps](https://github.com/MohAyman3600/Multi-Vendor-Django-E-Commerce/blob/master/C4_model_arch/structurizr-59568-projectApps.png)

![mainflow](https://github.com/MohAyman3600/Multi-Vendor-Django-E-Commerce/blob/master/C4_model_arch/structurizr-59568-mainFlow.png)


## Getting Started

### Dependencies

* Python 3
* Django

### Installing

* Clone the project
* Install requirements

### Executing program

* run 
```
python manage.py makemigrations api
```
* run 
```
 python manage.py migrate
```
* run 
```
 python manage.py runserver
```

## Authors

[@Mohamed Ayman](https://www.linkedin.com/in/mohayman3600/)


## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the [MIT] License - see the LICENSE.md file for details



