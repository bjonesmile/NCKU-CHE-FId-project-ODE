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
    Fout1(m)
    
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


Fin1(m)$(ord(m) lt 240)..Fin(m)=e=Fin(m+1);
Fout1(m)$(ord(m) lt 240)..Fout(m)=e=Fout(m+1);

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