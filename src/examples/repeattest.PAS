BEGIN {REPEAT STATEMENT TEST}
	i := 0;
	
	REPEAT
		j := i;
		k := i;
	UNTIL j <= i;
	
	BEGIN {CALCULATE A SQRT}
		number := 4;
		root := number;
		
		REPEAT
			partial := number/root + root;
			root := partial/2;
		UNTIL root*root - number < 0.000001;
	END;
	WHILE x = 4 do y := 2; 
 	END.