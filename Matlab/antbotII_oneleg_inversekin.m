%inverse oneleg:
xprime1 = 370.987; %213.6188;
yprime1 = 0; %284.3948;
zprime1 = 172.155+14.9; %-155.7892+15.68;
xoffset1 = 141.33; %60.827;
X1 = xprime1-xoffset1;
yoffset1 = 0;%131.38;
Y1 = yprime1-yoffset1;
zoffset1 = +14.9;
Z1 = zprime1;
L1 = 66.5;
L2 = 92.17;
L3 = 193.66;
offsetang = 0;%pi/3;2*pi/3;pi;-pi/3;-2*pi/3   %%it can be selected
theta11 = atan2(Y1, X1)-offsetang;
% theta11 = pi-atan2(Y1, X1)-offsetang;
newx = cos(-1*offsetang)*X1 - sin(-1*offsetang)*Y1;
newy = sin(-1*offsetang)*X1 + cos(-1*offsetang)*Y1;
x1 = cos(theta11)*(newx) + sin(theta11)*(newy) - L1;
y1 = sin(theta11)*(newx) - cos(theta11)*(newy);
s1 = sqrt(x1^2 + zprime1^2);
t13 = acos(( s1^2 - L2^2 - L3^2)/(2*L2*L3));
theta13 = t13 - 53.27 *pi/180;
theta12 = - atan2(zprime1, x1) - atan2(L3*sin(t13), L2 + L3*cos(t13)) + (20)*pi/180;
theta11indegs1 = theta11*180/pi;
theta12indegs1 = theta12*180/pi*(-1);
theta13indegs1 = theta13*180/pi*(-1);
out = [theta11indegs1;theta12indegs1;theta13indegs1]
%%
t132 = -( acos(( s1^2 - L2^2 - L3^2)/(2*L2*L3)));
theta132 = t132 - 53.27 *pi/180;
theta122 =  atan2(zprime1, x1) + atan2(L3*sin(t132), L2 + L3*cos(t132)) - (20)*pi/180;
theta12indegs12 = theta122*180/pi*(1);
theta13indegs12 = theta132*180/pi*(-1);
out = [theta11indegs1 theta11indegs1;theta12indegs1 theta12indegs12;theta13indegs1 theta13indegs12]