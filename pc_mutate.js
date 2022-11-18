db = connect('mongodb://localhost/pcn');
db.pcnrp.aggregate( [
  {
     $addFields:
     {
 	bef_2013: {$lte: ["$tahun",2013]},
 	aft_2013: {$gt:  ["$tahun",2013]}
     }
  },

  {
     $switch: {
	branches: 
	[
	   {case: {pkt: {$in: ["PBT"]}}, then: "PBT & SETARAF"},
	   {case: {pkt: {$in: ["LKPL","LK I","LUK I"]}}, then: "LKPL & SETARAF"},
	   {case: {pkt: {$in: ["KPL","LUK","LK"]}}, then: "KPL & SETARAF"},
	   {case: {pkt: {$in: ["SJN","SJN(U)","BM"]}}, then: "SJN & SETARAF"}

	]
   }

  },

  {
     $match: {bef_2013: true}
  },

  {
     $group: {_id: "$pkt", min: {$min: "$pcn"}, maks: {$max: "$pcn"} }
  }

] )
