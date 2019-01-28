
syms a1 a2 real;
syms d1 d2 d3 d4 real;


%DH Parameter Table ( Modified )
dh = [-pi/2, 0, d1, -pi/2; -pi/2, a1, d2, -pi/2;pi/2 a2 d3 0; 0 0 d4 0];
    

for i = 1:4
    T(:, :, i) = [cos(dh(i, 4)), -sin(dh(i, 4)), 0, dh(i, 2); sin(dh(i, 4)) * cos(dh(i, 1)), cos(dh(i, 4)) * cos(dh(i, 1)), -sin(dh(i, 1)), -sin(dh(i, 1)) * dh(i, 3); sin(dh(i, 4)) * sin(dh(i, 1)), cos(dh(i, 4)) * sin(dh(i, 1)), cos(dh(i, 1)), cos(dh(i, 1)) * dh(i, 3); 0, 0, 0, 1];    
end


T_0_1 = T(:, :, 1);
T_1_2 = T(:, :, 2);
T_2_3 = T(:, :, 3);
T_3_4 = T(:, :, 4);

T_0_2 = T_0_1 * T_1_2;
T_0_3 = T_0_1 * T_1_2 * T_2_3;
T_0_4 = T_0_1 * T_1_2 * T_2_3 * T_3_4;

