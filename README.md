# Project Title

Multi-Vendor Django E-Commerce Website with Stripe Support.

## Description

An e-commerce website built using the Django Framework. The website has vendor and customer user profile types with ability to extend to other profile types; different permissions are set bsded on the profile type. Moreover, the webiste has cart app that works using session variables. Also, there is an orders app that uses Stripe for proccessing payments. The wesite templates was built by customizing free HTML temaplate from [@neha](neha@gmail.com), using Django template language. Tests are only set up for the users app, and checked using coverage package.

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

[@Mohamed Ayman](https://www.linkedin.com/in/mohamed-ayman-311628141/)


## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the [MIT] License - see the LICENSE.md file for details



