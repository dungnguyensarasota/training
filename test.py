from scipy.stats import linregress
x2 = 43648.41
x1 = -1405.37
y1 = 4
y2 = 5
slope, intercept, r_value, p_value, std_err = linregress([x1,x2],[y1,y2])
print(slope,intercept)