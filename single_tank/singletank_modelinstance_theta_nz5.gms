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
            fobj        object function
            ;
        qout.lo(m) = 0;
        qout.up(m) = 0.7; 

        eq(m)$(ord(m) lt 800) ..   A*(h(m+1)-h(m)) =e=  1/2*(theta(m+1)-qout(m+1)+theta(m)-qout(m)) ;
        uncertain(m) ..            theta(m) =e= (0.5+0.5*FId*theta_vertex(m)) ;
        ineq1(m) ..                h(m) =l= 10 ;
        ineq2(m) ..                h(m) =g= 1 ;

        qout1(m)$(ord(m) lt 160).. qout(m) =e= qout(m+1);
        qout2(m)$((ord(m) gt 160) and (ord(m) lt 320))..                qout(m) =e= qout(m+1);
        qout3(m)$((ord(m) gt 320) and (ord(m) lt 480))..                qout(m) =e= qout(m+1);
        qout4(m)$((ord(m) gt 480) and (ord(m) lt 640))..                qout(m) =e= qout(m+1);
        qout5(m)$((ord(m) gt 640) and (ord(m) lt 800))..                qout(m) =e= qout(m+1);
        h.fx('1') = h0;

        fobj .. obj =e= FId ;
        Model singletank /all/ ;
        Scalar ms 'model status', ss 'solve status' ;
        