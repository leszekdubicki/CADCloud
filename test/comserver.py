class HelloWorld:
	_reg_clsid_ = "{DC14B301-F205-485D-8F29-DCAB846A90CC}"
	_reg_desc_ = "Python Test COM Server"
	_reg_progid_ = "Python.TestServer"
	_public_methods_ = ['Hello']
	_public_attrs_ = ['softspace', 'noCalls']
	_readonly_attrs_ = ['noCalls']
	def __init__(self):
		self.softspace = 1
		self.noCalls = 0
	def Hello(self, who):
		self.noCalls = self.noCalls + 1
		# insert "softspace" number of spaces
		return "Hello" + " " * self.softspace + str(who)

if __name__=='__main__':
	# ni only for 1.4!
	import win32com.server.register
	win32com.server.register.UseCommandLine(HelloWorld)