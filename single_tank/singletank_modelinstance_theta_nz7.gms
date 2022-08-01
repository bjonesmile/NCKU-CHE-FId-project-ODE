        Sets
            m      discretize of time horizon /1*800/;
        Parameters
            A      bottom area of tank    /5/
            h0     initial value for stata var h /5.0/
            theta_vertex(m)
        ;
        theta_vertex(m) = 1;
        Variables
            qout(m)     flow rate of water out of tank controlled by valve
            obj         object value
            FId         flexibility index
            ;
        Positive Variable
            h(m)        height of tank
            theta(m)    uncertainty parameter
            ;
        Equations
            eq(m)       'A*dh/dt=theta-qout'
            ineq1(m)    h upper-bound
            ineq2(m)    h lowwer-bound
            uncertain(m)
            qout1(m)
            qout2(m)
            qout3(m)
            qout4(m)
            qout5(m)
            qout6(m)
            qout7(m)
            fobj        object function
            ;
        qout.lo(m) = 0;
        qout.up(m) = 0.7; 

        eq(m)$(ord(m) lt 800) ..   A*(h(m+1)-h(m)) =e=  1/2*(theta(m+1)-qout(m+1)+theta(m)-qout(m)) ;
        uncertain(m) ..            theta(m) =e= (0.5+0.5*FId*theta_vertex(m)) ;
        ineq1(m) ..                h(m) =l= 10 ;
        ineq2(m) ..                h(m) =g= 1 ;

        qout1(m)$(ord(m) lt 114).. qout(m) =e= qout(m+1);
        qout2(m)$((ord(m) gt 114) and (ord(m) lt 228))..                qout(m) =e= qout(m+1);
        qout3(m)$((ord(m) gt 228) and (ord(m) lt 342))..                qout(m) =e= qout(m+1);
        qout4(m)$((ord(m) gt 342) and (ord(m) lt 457))..                qout(m) =e= qout(m+1);
        qout5(m)$((ord(m) gt 457) and (ord(m) lt 571))..                qout(m) =e= qout(m+1);
        qout6(m)$((ord(m) gt 571) and (ord(m) lt 685))..                qout(m) =e= qout(m+1);
        qout7(m)$((ord(m) gt 685) and (ord(m) lt 800))..                qout(m) =e= qout(m+1);
        h.fx('1') = h0;

        fobj .. obj =e= FId ;
        Model singletank /all/ ;
        Scalar ms 'model status', ss 'solve status' ;
        