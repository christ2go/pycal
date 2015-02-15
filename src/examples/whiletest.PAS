BEGIN
	i := 0; j := 0;
	
	WHILE i = j DO k := i;
	
	BEGIN
		number := 2;
		root := number;
		
		while ( root*root - number < 0.001 ) DO BEGIN
			root := (number/root + root)/2;
			x := 2/3;
		END
	END;
END.