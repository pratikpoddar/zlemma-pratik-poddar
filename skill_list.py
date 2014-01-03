# Skill List from ckoverflow and Math.Stackexchange
skill_list=['pattern-recognition', 'opengl', 'c-sharp', 'ruby-on-rails', 'graph', 'fortran', 'matlab', 'multithreading', 'jquery', 'python', 'rake', 'powershell', 'neural-network', 'ms-access', 'linear-programming', 'lisp', 'set-theory', 'mapreduce', 'c++', 'parallel-programming', 'complexity-theory', 'calculus', 'statistical-inference', 'computer-vision', 'mysql', 'nonlinear-optimization', 'numerical-optimization', 'scala', 'algebra', 'functional-analysis', 'mahout', 'optimization', 'amazon-web-services', 'real-analysis', 'computational-geometry', 'javascript', 'ajax', 'apache', 'integer-programming', 'solr', 'search', 'vb', 'convex-optimization', 'text-mining', 's', 'swing', 'query-optimization', 'clojure', 'probability', 'haskell', 'linear-algebra', 'perl', 'maple', 'genetic-algorithm', 'statistics', 'java', 'combinatorics', 'automata', 'data-structures', 'numerical-methods', 'game-programming', 'scheme', 'discrete-optimization', 'c', 'hive', 'groovy', 'erlang', 'data-mining', 'image-processing', 'r', 'computation-theory', 'prolog', 'approximation-algorithms', 'web-scraping', 'actionscript', 'discrete-mathematics', 'number-theory', 'fsharp', 'measure-theory', 'regression', 'cassandra', 'asp.net', 'servlets', 'mathematica', 'hadoop', 'html', 'machine-learning', 'vhdl', 'bigdata', 'estimation-theory', 'jsp', 'sql', 'php', 'mathematical-modeling', 'algorithm', 'database', 'information-theory', 'django', 'oracle', 'coding-theory', 'formal-methods', 'graphics', 'finite-element-analysis', 'networks', 'information-retrieval', 'nlp', 'virtualization', 'differential-equations', 'computational-mathematics', 'time-series', 'programming-languages', 'visualization', 'compiler', 'mathematical-analysis', 'mathematical-physics', 'cryptography', 'software-engineering', 'operating-systems', 'stochastic-calculus', 'control-theory', 'bioinformatics', 'security', 'signal-processing', 'distributed-system', 'fluid-dynamics', 'chemistry', 'econometrics', 'artificial-intelligence', 'hci', 'game-theory', 'operations-research', 'functional-programming', 'data-modeling', 'ios', 'android']

# Skill List for Languages from Dmoz
skill_list_dmoz_lang = ['Assembly', 'Awk', 'C', 'C++', 'Cg', 'Clojure', 'Cocoa', 'C-sharp', 'Erlang', 'Fortran', 'Groovy', 'Haskell', 'HTML', 'Java', 'JavaScript', 'Lisp', 'Maple', 'Mathematica', 'MATLAB', 'OCaml', 'Objective-C', 'Pascal', 'Perl', 'PHP', 'PLSQL', 'Prolog', 'Python', 'R', 'SAS', 'Scheme', 'SQL', 'Verilog', 'VHDL']

# Skill List from Quant Stackexchange
skill_list_finance_stackoverflow = ['options', 'volatility', 'time-series', 'equities', 'fixed-income', 'statistics', 'interest-rates', 'backtesting', 'quant-trading-strategies', 'portfolio-management', 'trading', 'high-frequency', 'risk-management', 'market-data', 'optimization', 'fx', 'futures', 'monte-carlo', 'probability', 'regression', 'derivatives', 'stochastic-calculus', 'arbitrage', 'hedging', 'garch', 'yield-curve', 'swaps', 'market-microstructure', 'pairs-trading', 'machine-learning', 'capm', 'econometrics', 'numerical-methods', 'algorithmic-trading', 'american-options', 'forward', 'etf', 'credit', 'order-execution', 'visualization', 'exotics', 'financial-engineering', 'differential-equations', 'credit-ratings', 'asset-pricing', 'matlab']

skill_list_electrical_stackoverflow = ['arduino', 'microcontroller', 'power-supply', 'power', 'transistors', 'batteries', 'capacitor', 'pcb', 'usb', 'digital-logic','op-amp', 'circuit', 'current', 'fpga', 'resistors', 'mosfet', 'audio', 'voltage-regulator', 'motor', 'switches', 'amplifier', 'rf', 'serial', 'analog', 'integrated-circuit', 'wireless', 'ac', 'dc', 'transformer', 'verilog', 'diodes', 'c', 'vhdl', 'dc-motor', 'lcd', 'ethernet', 'bluetooth', 'raspberry-pi', 'radio', 'antenna', 'inductor', 'solar-cell', 'oscilloscope', 'electromagnetism', 'wifi', 'infrared', 'xilinx', 'microprocessor', 'pcb-fabrication', 'low-power']

#import itertools
#for comb in itertools.permutations(skill_list,2):
#	if comb[0]==comb[1]:
#		print "Same " + comb[0] + " " + comb[1]
#	if comb[0]==comb[1]+"s":
#		print "Extra s " + comb[0] + " " + comb[1]
#	if (comb[0] in comb[1]) and len(comb[0])>=3:
#		print "Almost same " + comb[0] + " " + comb[1]
#	if comb[0].replace('theory','').replace('-','')==comb[1].replace('theory','').replace('-',''):
#		print "Same " + comb[0] + " " + comb[1]	
#	if comb[0].replace('theory','').replace('-','')==comb[1].replace('theory','').replace('-','')+"s":
#		print "Extra s " + comb[0] + " " + comb[1]

skill_list = skill_list + skill_list_finance_stackoverflow + skill_list_dmoz_lang
skill_list = list(set(map(lambda x: x.lower().replace(' ','-'), skill_list)))

