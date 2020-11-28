# Storefront
t is a program to calculate and print a statement of a customer's charges at a book rental store.
It is divided into 3 stories.

## Story 1
Customers can rent the books from the store. The rent changes will be calculated on the basis
of the number of books rented and durations for each book it was rented. Per day rental charge
is $ 1.

## Story 2:
There are three kinds of books: regular, fiction, and novels. For Regular books renting per day
charge is $. 1.5. For fiction book renting per day, charge is $. 3. For novels, the per-day charge
is $. 1.5.

## Story 3:
The store decided to alter the calculations for Regular books and novels. Now for Regular books
for the first 2 days charges will be $ 1 per day and $ 1.5 thereafter. Minimum changes will be
considered as $ 2 if days rented is less than 2 days. Similarly for Novel minimum charges are
introduced as $ 4.5 if days rented is less than 3 days

## Setup
The project is built using Django 
To run this project, install docker and docker-compose installed on your machine

```
$ docker-compose up
```
