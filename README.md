<!-- OVERVIEW -->

---

## this is my first time creating a README.md and kinda feels new but also good to explain my project from head to tail...thanks

## a database created with SQLite3
## a connection created into a flask g as 'conn' variable separated function with close conn auch separated

## using a flask app to power the python engine
## with app.context create a start-up connection and create table and use the teardown.context to auto close connection after each route

## see app.py with structural view of code...

<!-- TECH sTACk -->

-- Flask
--SQLite
--Flask-jwt-extended
-- written in PYTHON 🐍

<!-- EnD-PoinTa -->

--users
--auth
--products
--add_to_cart
--check_out

<!-- SET-uP AND ruN -->

--clone Repo
--install requirements...see in requirement.txt
-- in terminal run (python app.py)

<!-- EnD-Points -->
--AUTH --/Login---/register....methods = POST
--USER --/user/me methods = PUT  /user/me methods =GET
--products --/product GET and POST --/products methods GET /products/<int:product_id> methods = GET or PUT
--CART -GET,PUT,POST
--ORDER -- POST
--see folder routes,has all route.py
--each route file has a url_prefix,see each blueprint(url-prefix)

<!-- hints -->

--seed admin to access product creation and other admin required end_points With sql
  "UPDATE users SET is_admin =?,where email = ?",(1,yourmail@mail.com,)

