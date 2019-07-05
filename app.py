from flask import Flask, render_template, redirect, request, abort, session, jsonify
from flask_session import Session
from wsgiref.simple_server import make_server
from formulaTransform import intoBrackets, getOrderList, getOriginalFormula, removeBrackets, iff_imp_Convert, deMorgen_Convert
from simpli import deleteSameVar, deleteContradictionVar, deleteSameSentence
from distri import distribution, runDistributionEachElement, changeToOppositeForm
import re
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/input')
def input():

		formula = request.args.get("formula")

		if re.search('\d+', formula):
			print("Do not accept number in formula")
			sys.exit()

		DNF = []
		CNF = []
		resultList = []
		
#		======
		orderList = getOrderList(formula)
		print(orderList)
#		=======
		orderList = iff_imp_Convert(orderList)
		formula = getOriginalFormula(orderList)
		if formula not in resultList:
			resultList.append(formula)
#		print(orderList)

#		here we have to rebuild the orderList to be the form we can handle
#		e.g.['p or ~ q', '~ p or r', '(0 and 1) or (~ 0 and ~ 1)', '~ 2 or r'] => 
#		    ['p or ~ q', '~ p or r', '0 and 1', 'p or ~ q', '~ p or r', '~ 3 and ~ 4', '2 or 5', '~ 6 or r']

		orderList = getOrderList(formula)
#		print(orderList)

#		do the deMorgen_Convert() as many as possible until all the parts are well done
#		====================================================
		tempOrderList = []
		while orderList != tempOrderList:

			tempOrderList = orderList.copy()
			orderList = deMorgen_Convert(orderList)

#		print(orderList)

		formula = getOriginalFormula(orderList)
		if formula not in resultList:
			resultList.append(formula)
#		print(formula)

		formula = removeBrackets(orderList)

		if formula not in resultList:
			resultList.append(formula)

		orderList = getOrderList(formula)

#		print(orderList)

		formula = distribution(orderList)
		if formula not in resultList:
			resultList.append(formula)

#		print(formula)
#		formula = "(r and ~ p) or (q and ~ p and ~ r) or (q and ~ p and ~ r) or (q and r and ~ p and ~ r) or (p and q and ~ p and ~ r) or (p and ~ p and ~ r) or (p and r and ~ p and ~ r) or (q and r and ~ p and ~ r) or (r and ~ p and ~ r) or (r and ~ p and ~ r) or (q and r and ~ p) or (q and r and ~ p and ~ r) or (q and r and ~ p) or (p and q and r and ~ p) or (p and r and ~ p and ~ r) or (p and r and ~ p) or (q and r and ~ p) or (r and ~ p and ~ r) or (r and ~ p) or (p and q and ~ p) or (p and q and ~ p and ~ r) or (p and q and r and ~ p) or (p and q and ~ p) or (p and ~ p and ~ r) or (p and r and ~ p) or (p and q and r and ~ p) or (p and r and ~ p and ~ r) or (p and r and ~ p) or (p and q and ~ p and ~ r) or (p and q and ~ p and ~ r) or (p and q and r and ~ p and ~ r) or (p and q and ~ p and ~ r) or (p and ~ p and ~ r) or (p and r and ~ p and ~ r) or (p and q and r and ~ p and ~ r) or (p and r and ~ p and ~ r) or (p and r and ~ p and ~ r) or (p and q and r and ~ p) or (p and q and r and ~ p and ~ r) or (p and q and r and ~ p) or (p and q and r and ~ p) or (p and r and ~ p and ~ r) or (p and r and ~ p) or (p and q and r and ~ p) or (p and r and ~ p and ~ r) or (p and r and ~ p) or (q and r and ~ p) or (q and r and ~ p and ~ r) or (q and r and ~ p) or (p and q and r and ~ p) or (p and r and ~ p and ~ r) or (p and r and ~ p) or (q and r and ~ p) or (r and ~ p and ~ r) or (r and ~ p) or (q and r and ~ p and ~ r) or (q and r and ~ p and ~ r) or (q and r and ~ p and ~ r) or (p and q and r and ~ p and ~ r) or (p and r and ~ p and ~ r) or (p and r and ~ p and ~ r) or (q and r and ~ p and ~ r) or (r and ~ p and ~ r) or (r and ~ p and ~ r) or (q and r and ~ p) or (q and r and ~ p and ~ r) or (q and r and ~ p) or (p and q and r and ~ p) or (p and r and ~ p and ~ r) or (p and r and ~ p) or (q and r and ~ p) or (r and ~ p and ~ r) or (r and ~ p) or q"
		orderList = getOrderList(formula)
#		print(orderList)
		orderList = deleteSameVar(orderList)
#		print(getOriginalFormula(orderList))
		orderList = deleteContradictionVar(orderList)
#		print(getOriginalFormula(orderList))
		orderList = deleteSameSentence(orderList)
#		 print(orderList)
		formula = getOriginalFormula(orderList)
#		orderList = changeToOppositeForm(orderList)
		if formula not in resultList:
			resultList.append(formula)

		if len(orderList) <= 1:
			DNF.append(getOriginalFormula(orderList))
			CNF.append(DNF[-1])
		else:
			if "or" in orderList[-1]:
				DNF.append(getOriginalFormula(orderList))
				orderList = changeToOppositeForm(orderList)
				if len(orderList) <= 1:
					DNF.append(getOriginalFormula(orderList))
				CNF.append(getOriginalFormula(orderList))
			else:
				CNF.append(getOriginalFormula(orderList))
				orderList = changeToOppositeForm(orderList)
				if len(orderList) <= 1:
					CNF.append(getOriginalFormula(orderList))
				DNF.append(getOriginalFormula(orderList))

		print(resultList)
		output = {'dnf': min(DNF, key=len), 'cnf': min(CNF, key=len)}

		return jsonify(output)

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
