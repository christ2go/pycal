BEGIN
	CASE i+1 OF
		1 :		j := i;
		4 :		j := 4*i;
		3,2,5:	j := 523*i;
	END
END.