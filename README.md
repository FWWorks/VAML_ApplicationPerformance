# VAML_ApplicationPerformance
Course project for VAML. Focus on visualization of application performance.

Requirement
1 - use Chrome
2 - Flask/pandas/sklearn installed
3 - make sure your localhost:5000 port isn't occupied by other applications

How to run
1 - get into final_submission directory
2 - get into Include directory
3 - execute 'python test.py' under that directory
4 - open 'Chrome' browser
5.a - type in '127.0.0.1:5000/pmd' in address to view performance analysis for 'pmd' application
5.b - type in '127.0.0.1:5000/blackscholes' in address to view performance analysis for 'blackscholes' application

Tips
1 - Selecting time periods in line chart(Performance view) takes time to update other views.
2 - If you hover on parallel coordinates views or click on data items in them, you need to double click on PCPs to recover prior to your interactions with other plots. Because I set a block on it to make viewing other plots in down page easier.
3 - If you brush on coordinates in PCPs, a rectangle appears on the coordinate. Remember to click on the other part of that coordinate to cancel selection prior to other interactions. (Because I also set a block on it.)
4 - If you find the selection in line chart(Performance view) goes wrong, double click on PCPs to make it recover because you are highly possible trigger the hover event on PCPs. 

Interactions 