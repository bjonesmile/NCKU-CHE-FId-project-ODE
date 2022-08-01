Sets
    m/1*240/;
Parameters
    Pm/100/
    Ks/10/
    Ycs/0.07/
    Yps/0.44/
    Sa_vertex(m)
    T_vertex(m)
    ;

Sa_vertex(m) = 1;
T_vertex(m) = 1;

Positive variables
*dynamic flexibility indes
    FId
*s.v.
    S(m)
    C(m)
    P(m)
    V(m)
    mu(m)
    mu0(m)
*m.v.
    Fin(m)
    Fout(m)
*uncertain parameter
    Sa(m)
    T(m)
    ;
Variables
    obj;
Equations
    eq1(m)
    eq2(m)
    eq3(m)
    eq4(m)
    eq11(m)
    eq12(m)
    
    uncertanSa(m)
    uncertanT(m)
    
    Fin1(m)
    Fin2(m)
    Fin3(m)
    Fin4(m)
    Fin5(m)
    Fin6(m)
    Fin7(m)
    Fin8(m)
    Fin9(m)
    Fin10(m)
    Fin11(m)
    Fin12(m)
    Fin13(m)
    Fin14(m)
    Fin15(m)
    Fout1(m)
    Fout2(m)
    Fout3(m)
    Fout4(m)
    Fout5(m)
    Fout6(m)
    Fout7(m)
    Fout8(m)
    Fout9(m)
    Fout10(m)
    Fout11(m)
    Fout12(m)
    Fout13(m)
    Fout14(m)
    Fout15(m)
    
    fobj;

eq1(m)$(ord(m) lt 240)..S(m+1)-S(m)=e=1/2*(-1/Ycs*mu(m)*C(m)+Fin(m)*Sa(m)/V(m)-Fout(m)*S(m)/V(m)
                                           -1/Ycs*mu(m+1)*C(m+1)+Fin(m+1)*Sa(m+1)/V(m+1)-Fout(m+1)*S(m+1)/V(m+1));
eq2(m)$(ord(m) lt 240)..C(m+1)-C(m)=e=1/2*(mu(m)*C(m)-Fout(m)*C(m)/V(m)
                                          +mu(m+1)*C(m+1)-Fout(m+1)*C(m+1)/V(m+1));
eq3(m)$(ord(m) lt 240)..P(m+1)-P(m)=e=1/2*(Yps/Ycs*mu(m)*C(m)-Fout(m)*P(m)/V(m)
                                          +Yps/Ycs*mu(m+1)*C(m+1)-Fout(m+1)*P(m+1)/V(m+1));
eq4(m)$(ord(m) lt 240)..V(m+1)-V(m)=e=1/2*(Fin(m)-Fout(m)
                                          +Fin(m+1)-Fout(m+1));
eq11(m)..mu(m)=e=mu0(m)*S(m)/(Ks+Sa(m))*(1-P(m)/Pm);
*eq12(m)..mu0(m)=e=power((0.0216081*T(m)-0.02659972),2);
eq12(m)..mu0(m)=e=-0.000049205*(T(m)**4)+0.00569477*(T(m)**3)-0.24584*(T(m)**2)+4.7132*T(m)-33.435;

uncertanT(m) .. T(m)=e=(25+10*FId*T_vertex(m));
uncertanSa(m) .. Sa(m)=e=(100+50*FId*Sa_vertex(m));

Fin1(m)$(ord(m) lt 16)..Fin(m)=e=Fin(m+1);
Fin2(m)$((ord(m) gt 16) and (ord(m) lt 32))..Fin(m)=e=Fin(m+1);
Fin3(m)$((ord(m) gt 32) and (ord(m) lt 48))..Fin(m)=e=Fin(m+1);
Fin4(m)$((ord(m) gt 48) and (ord(m) lt 64))..Fin(m)=e=Fin(m+1);
Fin5(m)$((ord(m) gt 64) and (ord(m) lt 80))..Fin(m)=e=Fin(m+1);
Fin6(m)$((ord(m) gt 80) and (ord(m) lt 96))..Fin(m)=e=Fin(m+1);
Fin7(m)$((ord(m) gt 96) and (ord(m) lt 112))..Fin(m)=e=Fin(m+1);
Fin8(m)$((ord(m) gt 112) and (ord(m) lt 128))..Fin(m)=e=Fin(m+1);
Fin9(m)$((ord(m) gt 128) and (ord(m) lt 144))..Fin(m)=e=Fin(m+1);
Fin10(m)$((ord(m) gt 144) and (ord(m) lt 160))..Fin(m)=e=Fin(m+1);
Fin11(m)$((ord(m) gt 160) and (ord(m) lt 176))..Fin(m)=e=Fin(m+1);
Fin12(m)$((ord(m) gt 176) and (ord(m) lt 192))..Fin(m)=e=Fin(m+1);
Fin13(m)$((ord(m) gt 192) and (ord(m) lt 208))..Fin(m)=e=Fin(m+1);
Fin14(m)$((ord(m) gt 208) and (ord(m) lt 224))..Fin(m)=e=Fin(m+1);
Fin15(m)$((ord(m) gt 224) and (ord(m) lt 240))..Fin(m)=e=Fin(m+1);

Fout1(m)$(ord(m) lt 16)..Fout(m)=e=Fout(m+1);
Fout2(m)$((ord(m) gt 16) and (ord(m) lt 32))..Fout(m)=e=Fout(m+1);
Fout3(m)$((ord(m) gt 32) and (ord(m) lt 48))..Fout(m)=e=Fout(m+1);
Fout4(m)$((ord(m) gt 48) and (ord(m) lt 64))..Fout(m)=e=Fout(m+1);
Fout5(m)$((ord(m) gt 64) and (ord(m) lt 80))..Fout(m)=e=Fout(m+1);
Fout6(m)$((ord(m) gt 80) and (ord(m) lt 96))..Fout(m)=e=Fout(m+1);
Fout7(m)$((ord(m) gt 96) and (ord(m) lt 112))..Fout(m)=e=Fout(m+1);
Fout8(m)$((ord(m) gt 112) and (ord(m) lt 128))..Fout(m)=e=Fout(m+1);
Fout9(m)$((ord(m) gt 128) and (ord(m) lt 144))..Fout(m)=e=Fout(m+1);
Fout10(m)$((ord(m) gt 144) and (ord(m) lt 160))..Fout(m)=e=Fout(m+1);
Fout11(m)$((ord(m) gt 160) and (ord(m) lt 176))..Fout(m)=e=Fout(m+1);
Fout12(m)$((ord(m) gt 176) and (ord(m) lt 192))..Fout(m)=e=Fout(m+1);
Fout13(m)$((ord(m) gt 192) and (ord(m) lt 208))..Fout(m)=e=Fout(m+1);
Fout14(m)$((ord(m) gt 208) and (ord(m) lt 224))..Fout(m)=e=Fout(m+1);
Fout15(m)$((ord(m) gt 224) and (ord(m) lt 240))..Fout(m)=e=Fout(m+1);

fobj..obj=e=FId;

*flexibility
    FId.lo= 0;
    FId.up= 1.0;
*setting lower bound for m.v.
    Fin.lo(m)=0.01;
    Fout.lo(m)=0.05;
*setting upper bound for m.v.
    Fin.up(m)=0.5;
    Fout.up(m)=0.5;
*setting lower bound for s.v.
    S.lo(m)= 0.5;
    C.lo(m)= 0;
    P.lo(m)= 40;
    V.lo(m)= 1.5;
*setting upper bound for s.v.
    S.up(m)= 80;
    C.up(m)= 15;
*    P.up(m)= 100;
    V.up(m)= 5;
*initial condition
    S.fx('1')=4.5;
    C.fx('1')=5;
    P.fx('1')=50;
    V.fx('1')=1.5;

model alcoholicCSTR /all/;