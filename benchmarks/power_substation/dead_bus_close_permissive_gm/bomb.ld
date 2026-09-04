// Dead Bus Close Permissive : BOMB baseline
// Defect: Allows close when both buses are live, ignoring synchronization
OTE(tie_close) := XIC(req_close) * XIO(bus1_live) + XIC(req_close) * XIO(bus2_live) + XIC(req_close) * XIC(bus1_live) * XIC(bus2_live) ;
