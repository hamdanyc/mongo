db.pcnrp.aggregate( [
  {
    $addFields: { 
    	bef_2013: {$lte: ["$tahun",2013]},
    	aft_2013: {$gt:  ["$tahun",2013]}
    	}
  }     
] )
