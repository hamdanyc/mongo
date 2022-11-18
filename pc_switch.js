db = connect('mongodb://localhost/pcn');
db.pcnrp.aggregate( [
{
   $project:
   {
        "pkt": 1,
        "rank":
        {
            $switch:
        {
	    branches:
	      [
		   {case: {$in: ["$pkt",["PBT","APPR"]]}, then: "PBT & SETARAF"},
		   {case: {$in: ["$pkt",["LKPL","LU I","LK I"]]}, then: "LKPL & SETARAF"},
		   {case: {$in: ["$pkt",["KPL","LU II","LK II","LUK"]]}, then: "KPL & SETARAF"},
		   {case: {$in: ["$pkt",["SJN","SJN U","BM"]]}, then: "SJN & SETARAF"},
		   {case: {$in: ["$pkt",["SSJN","F/SJN","BK"]]}, then: "SSJN & SETARAF"},
		   {case: {$in: ["$pkt",["PW II","PW U II"]]}, then: "PW II & SETARAF"},
		   {case: {$in: ["$pkt",["PW I","PW U I"]]}, then: "PW I & SETARAF"},
		   {case: {$in: ["$pkt",["KAPT","KAPT(TUDM)"]]}, then: "KAPT & SETARAF"},
		   {case: {$in: ["$pkt",["MEJ","LT KDR TLDM","MEJ(TUDM)"]]}, then: "MEJ & SETARAF"},
		   {case: {$in: ["$pkt",["LT KOL","KDR TLDM","LT KOL(TUDM)"]]}, then: "LT KOL & SETARAF"},
		   {case: {$in: ["$pkt",["KOL","KEPT TLDM","KOL(TUDM)"]]}, then: "KOL & SETARAF"},
		   {case: {$in: ["$pkt",["BRIG JEN","LAKSMA","BRIG JEN(TUDM)"]]}, then: "BRIG JEN & SETARAF"},
		   {case: {$in: ["$pkt",["MEJ JEN","LAKSDA","MEJ JEN(TUDM)"]]}, then: "MEJ JEN & SETARAF"},
		   {case: {$in: ["$pkt",["LT JEN","LAKSDYA","LT JEN(TUDM)"]]}, then: "LT JEN & SETARAF"},
		   {case: {$in: ["$pkt",["JEN","LAKSMANA","JEN(TUDM)"]]}, then: "JEN & SETARAF"},
		   {case: {$in: ["$pkt",["PAT"]]}, then: "PAT & SETARAF"}
	      ],
              default: "ralat"
        }
       }
   }
}
] )
