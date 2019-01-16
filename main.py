import os, sys

from itertools import combinations
class PAI:
	def __init__(self):
		self.log_state = True
		self.VARIABLE = "<class 'variable'>"

		self.EXECUTIONS = ['[assignment]']
		self.EQUALITY_OPERATORS = ['=', 'is']
		self.QUESTIONERS = ['what', 'how']
		
		self.models = {}
		self.environment = {}

		self.generateTraining()
		self.train()

	def chekExecution(self, execution):
		if execution in self.EXECUTIONS:
			return True

		try:
			eval(execution)
			return True

		except Exception as e:
			return False

	def generateTraining(self):
		'''
		generate the training file for the std lib of pai
		'''
		training_data = []

		# for assignment
		variables = {'some name':'3', 'x':'2.5', 'cart':"'a'", 'var_name':"'gate man'"}
		execution = 'self.environment'
		similar_codes = ['is', '=']
		for code in similar_codes:
			for variable_name in variables:
				variable_value = variables[variable_name]
				td = '{} {} {} ~ {} {} {}\n'.format(variable_name, code, variable_value, execution, variable_name, variable_value)
				training_data.append(td)

		variables = {'2':'3', 'x':'15', '9':'var_name', '2.5':'10', '7': '10.5', "'hello'":"'world'", '[1,2]':'[5]', '[1,2]':'[5]'}
		similar_codes = {'+':['sum', 'add'], '*':['product of', 'find product of', 'multiply']}
		for execution in similar_codes:
			for code in similar_codes[execution]:
				for variable_name in variables:
					variable_value = variables[variable_name]
					td = '{} {} and {} ~ {} {} {}\n'.format(code, variable_name, variable_value, variable_name, execution, variable_value)
					training_data.append(td)

		# for assignment
		outputs = ['x', '3', '[1,2,3,4]', "'hello world!'", '{1:2,3:4}']
		execution = 'print'
		similar_codes = ['print', 'show', 'display', 'what is ']
		for code in similar_codes:
			for output in outputs:
				variable_value = variables[variable_name]
				td = '{} {} ~ {} {}\n'.format(code, output, execution, output)
				training_data.append(td)


		# open the file and read the lines of code
		with open('pai.std.lib', 'w') as file:
			file.writelines(training_data)

		return

	def interpret(self, code):
		print('code:{}'.format(code))
		if self.isAssignment(code):
			print('template: [assignment]')
			return
		
		template, var_template = self.parse(code)
		print('template:{}, var_template:{}'.format(template, var_template))

		status = True
		while status:
			for model in self.models:
				if model in template:
					print('  ->model:{} found in template'.format(model))

					haystack = " ".join([x[:-1] if x.startswith('[var]') else x for x in var_template.split()])
					pin = self.models[model]['template']

					start = haystack.index(pin)
					span = (start, start + len(pin) + haystack.split().count('[var]'))

					template_map = self.map(code, var_template)
					new_template_map = {x:template_map[x] for x in template_map if x in var_template[span[0]:span[1]]}


					result = self.run(model, self.models[model], new_template_map)

					if result == False:
						status = False
						continue

					template = template.replace(model, str(type(result)), 1)

					if template.startswith('<class '):
						return result

					tm = var_template[span[0]:span[1]]
					for x in new_template_map:
						tm = tm.replace(x, new_template_map[x], 1).strip()

					result = result if type(result) == str else str(result)
					code = code.replace(tm, result, 1)

					template, var_template = self.parse(code)
					print('template:{}, var_template:{}'.format(template, var_template))

					if self.isAssignment(code):
						print('template: [assignment]')
						return


	def isAssignment(self, code):
		model = self.parseAssignment(code)
		if model != None:
			a, b, model = model
			self.environment[a] = eval(b)
			return True
		return False

	def isPrimitive(self, code):
		try:
			if code not in self.environment:
				return str(type(eval(code)))
			return self.VARIABLE

		except NameError:
			# variable name not defined
			return False

		except Exception as e:
			# self.log(e)
			return False

	def log(self, output=''):
		if self.log_state:
			print(output)

	def map(self, s1, s2, delimeter=" "):
		'''
		x and y are strings, the function returns the similarity ratio and
		mapping relation of the strings
		'''
		a, b = s1.split(), s2.split()
		lw = a
		if len(b) < len(a):
			lw = b

		formats = [{"a":a, "b":b, "ca":0, "cb":0}]
		for w in set(lw):
			for f in formats:
				fa, fb, fca, fcb = f["a"], f["b"], f["ca"], f["cb"]
				fac, fbc = fa.count(w), fb.count(w)
				fai = [i for i, xx in enumerate(fa) if xx == w]
				fbi = [i for i, xx in enumerate(fb) if xx == w]
				if fbc < fac:
					lwc = fbc
					fa_combs = list(combinations(fai, lwc))
					fb_combs = [fbi for _ in fa_combs]

				else:
					lwc = fac
					fb_combs = list(combinations(fbi, lwc))
					fa_combs = [fai for _ in fb_combs]
				
				new_formats = []
				for n in range(len(fa_combs)):
					ca, cb = fca, fcb
					fax, fbx = fa.copy(), fb.copy()
					for i in range(lwc):
						fax[fa_combs[n][i]] = "`"
						fbx[fb_combs[n][i]] = "`"

						# self.log(fax, fbx, fa_combs[n][i], fb_combs[n][i], ca, cb)
					new_formats.append({"a":fax, "b":fbx, "ca":ca, "cb":cb})
			formats = new_formats.copy()

		for xx in formats:
			x, y = xx["a"], xx["b"]
			
			x_map, y_map = {}, {}
			xl = delimeter.join(self.trimVars(x)).split("`")
			yl = delimeter.join(self.trimVars(y)).split("`")

			for i in range(len(xl)):
				xl[i], yl[i] = xl[i].strip(), yl[i].strip()
				if xl[i] != '' and yl[i] != '':
					x_map[xl[i]] = yl[i]
					y_map[yl[i]] = xl[i]
		return y_map

	def parse(self, code):
		code = code.split(' ')
		if len(code) == 1:
			return code[0]

		template = []
		var_template = []
		c = 0
		for x in code:
			token = x.strip()
			is_primitive = self.isPrimitive(token)
			
			if is_primitive == False:
				x = self.parse(token)
				template.append(x)
				var_template.append(x)

			else:
				var_template.append('[var]{}'.format(c))
				template.append(is_primitive)
				c += 1
		
		template = " ".join(template)
		var_template = " ".join(var_template)
		return template, var_template

	def parseAssignment(self, code, execution=None):
		tokens = code.split()
		varz = []
		for equality_operator in self.EQUALITY_OPERATORS:

			if equality_operator in tokens and tokens.count(equality_operator) == 1:
				var = [x.strip() for x in code.split(equality_operator)]

				if len(var) != 2:
					continue

				if equality_operator == 'is' and var[0] in self.QUESTIONERS:
					continue

				var_val_primitive = self.isPrimitive(var[-1])
				varz.append({'0 0':self.VARIABLE})
				if var_val_primitive:
					key = var[-1].split()[0]
					if execution != None: varz.append(('{}'.format(var_val_primitive)))
					model_template = '[var] {} [var]'.format(equality_operator)
					model = '{} {} {}'.format(self.VARIABLE, equality_operator, var_val_primitive)
					var.append({model:{'var_type':varz, 'code':model_template}})
					return var

	def parseTraining(self, code, execution):
		model_template, template = execution, code

		execution = execution.split(' ')
		code = code.split(' ')
		
		common_elements = set(code).intersection(set(execution))

		last_index = len(code) - 1
		last_var_index = None

		var, varz = '', []
		model = code.copy()

		for i, e in enumerate(code):
			if (e not in common_elements and last_var_index != None) or (last_var_index == None and i == last_index):
				ix = i + 1 if i == last_index else i
				last_var_index = i if i == last_index and last_var_index == None else last_var_index

				var = " ".join(code[last_var_index:ix]).strip()
				var_is_primitive = self.isPrimitive(var)

				print('var = {}, isPrimitive = {}'.format(var, var_is_primitive))
				if var_is_primitive:
					key = var.split()[0]
					varz.append(('{}'.format(var_is_primitive)))
					for index in range(last_var_index, ix):
						model[last_var_index] = var_is_primitive if index == last_var_index else ''
						model_template = model_template.replace(var, '[var]', 1)
						template = template.replace(var, '[var]', 1)

			if e not in common_elements:
				last_var_index = None
				continue
			
			if last_var_index == None:
				last_var_index = i

		model = " ".join(model)
		return {model:{'var_type':varz, 'code':model_template, 'template':template}}

	def run(self, code, model, template_map):
		new_code, var_type = model['code'], model['var_type']

		for var in template_map:
			var_val = varx = template_map[var]
			if var.startswith('[var]'):
				var_index = int(var.replace('[var]', '', 1).strip())

			else:
				continue

			if var_type[var_index] == self.VARIABLE:
				if var_val in self.environment:
					varx = self.environment[var_val]
					varx = varx if type(varx) == str else str(varx)

				else:
					print('Variable "{}" has is not recognized'.format(var_val))

			new_code = new_code.replace('[var]', varx, 1)

		self.log('	  new_code:{}'.format(new_code))

		try:
			if new_code.startswith('print '):
				print(new_code.replace('print ', '', 1))
				return True
				
			else:
				ret = eval(new_code)

			return ret

		except Exception as e:
			print(e)
			return False

	def train(self, filepath='pai.std.lib'):
		# open the file and read the lines of code
		with open(filepath, 'r') as file:
			training = file.readlines()

		self.log('========================================training in progress=====================================\n')
		for training_pair in training:
			code, execution = training_pair.split('~')

			code, execution = code.strip(), execution.strip()
			self.log('code = [{}], execution = {}'.format(code, execution))

			model = self.parseAssignment(code, execution)
			if model == None:
				model = self.parseTraining(code, execution)

			else:
				a, b, model = model
				self.environment[a] = eval(b)

			print(model, end="\n\n")
			self.models.update(model)						
			self.log()
		self.log('========================================training is done=====================================\n')

		# rest environment to avoid conflict with intepreter code
		self.environment = {}
		return

	def trimVars(self, map_model, var="`"):
		'''
		to remove excess <vars> from a map
		'''
		#compress the <var>s
		while '{} {}'.format(var, var) in map_model:
			map_model = map_model.replace('{} {}'.format(var, var), var)

		return map_model
# get the file to interpret
args = sys.argv[1:]

# the PAI interpreter
PAI_interpreter = PAI()

def main():
	# check if the filepath is included
	if len(args) < 1:
		return

	# get the file path
	filepath = args[0]

	# open the file and read the lines of code
	with open(filepath, 'r') as file:
		source_code = file.readlines()

	# run the code
	for line_of_code in source_code:	
		code = line_of_code.replace('\n', '')
		PAI_interpreter.interpret(code)

		print()

if __name__ == '__main__':
	main()