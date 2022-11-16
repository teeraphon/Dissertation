//SPDX-License-Identifier: University of Southampton
pragma solidity ^0.8.0;

// import "./hardhat/console.sol";

contract Vouch{

    address contract_owner = msg.sender;
    address[] public nodes;
    address[] public ranked;
    address[] public punlishment_list;
    uint public reset_tokenPrice = 1 ether;


    event VouchLog(uint _time, address _from, address _to);

    struct VouchDetails {
        mapping(address => bool) vouchedBy;
        mapping(address => bool) vouchedTo;
        address[] vouchedByList;
        address[] vouchedToList;
        bool isVouched;
        bool isAdded;
        bool isinitVouchtoken;
        uint total_inbound_link;
        uint total_outbound_link;
        uint prScore;
        uint ranking;
        uint vouch_token;  
    }

    modifier VouchVerification(address _vouchTo) {
        //Check the node can vouch once on each account
        require(vouchedList[_vouchTo].vouchedBy[msg.sender] == false, "ERROR : This account already vouched by you.");
        //Check the node can not vouch on themself
        require(_vouchTo != msg.sender, "ERROR : Not allow to vouch yourself.");
        //check the vouch token initialize
        require(vouchedList[msg.sender].isinitVouchtoken == true, "ERROR : Vouch token does not init or reset.");
        //check right to make vouch
        require(vouchedList[msg.sender].vouch_token > 50, "ERROR : Not enough vouch token.");
        _;
    }

    modifier UnvouchVerification(address _unvouchTo) {
        require(vouchedList[_unvouchTo].vouchedBy[msg.sender] == true, "ERROR : This account not vouch yet, cannot unvouch.");
        _;
    }

    modifier setVouchTokenVerification(address _owner) {
        //
        require(msg.value == 1 ether, "ERROR : Token moust be purchase/ reset with 1 ETH.");
        _;
    }

    mapping(address => VouchDetails) public vouchedList;
    // mapping(address => uint) public total_inbound_link;
    // mapping(address => uint) public total_outbound_link;

    function Init_vouchToken(address _transac_owner) internal {
        vouchedList[_transac_owner].isinitVouchtoken = true;
        vouchedList[_transac_owner].vouch_token = 100;
    }

    function Init_score(address[] memory _nodes,uint _n) internal {

        uint nodesLength = _nodes.length;
        for(uint i = 0; i < nodesLength; i++) {
            vouchedList[_nodes[i]].prScore = 100 / _n;
            //Print score for debug
            //console.log(vouchedList[_nodes[i]].prScore);
        }

    }

    function nodes_punishment(address _node, uint _allnodesnum) internal {
        uint punishment_cost = 100 / (_allnodesnum - 1);
        vouchedList[_node].vouch_token -= punishment_cost;
    }

    function PagerankCal(address[] memory _nodes, uint _n) internal {
        //Damping factor
        uint _alpha = 85;
        
        Init_score(_nodes, _n);
        //PageRank : PR(A) = 1 - d + d*(PR(Tn)/C(Tn)+....+...)
        uint nodesLength = _nodes.length;

        //Secure iteration for let score reach convergence
        for(uint k = 0; k < 100; k++){

            for(uint i = 0; i < nodesLength; i++) {
                uint temp_score_sum;
                if(vouchedList[_nodes[i]].total_inbound_link == 0) {
                    // In case that node not have incoming link
                    vouchedList[_nodes[i]].prScore = 100 - _alpha;
                }else{
                    for(uint j = 0; j < vouchedList[_nodes[i]].vouchedByList.length; j++){
                        //Calculate sigma inbound node (PR(Tn)/C(Tn)+....+..)
                        address temp_inbound_node = vouchedList[_nodes[i]].vouchedByList[j];
                        require(vouchedList[temp_inbound_node].total_outbound_link != 0, "ERROR : Vouched account not have outbound link (Impossible) == BUG");
                        temp_score_sum += (vouchedList[temp_inbound_node].prScore) / vouchedList[temp_inbound_node].total_outbound_link;
                    }

                    // pr = (1 - d) + d(E PR(T)/C(T))
                    temp_score_sum = ((100 - _alpha) * 100) + ((_alpha) * temp_score_sum);
                    uint mod_test = temp_score_sum % 100;
                    if(temp_score_sum != mod_test){

                        vouchedList[_nodes[i]].prScore = temp_score_sum / 100;
                    }else {

                        vouchedList[_nodes[i]].prScore = temp_score_sum;
                    }
                    
                }

            }
        }
        ranked = SortNodeRanking(nodes);
        //Print score for debug
        // for(uint l = 0 ; l < ranked.length; l++){
        //     console.log(ranked[l]);
        // }
    }


    function SortNodeRanking(address[] memory unrank_nodes) internal view returns(address[] memory ranked_nodes){

        uint i;
        uint j;
        uint nodesLength = unrank_nodes.length;
        ranked_nodes = unrank_nodes;

        for (i = 0; i < nodesLength - 1; i++){
             // Last i elements are already 
            // in place
            for (j = 0; j < nodesLength - i - 1; j++){
                if (vouchedList[ranked_nodes[j]].prScore < vouchedList[ranked_nodes[j + 1]].prScore){
                    //swap(arr[j], arr[j + 1]);
                    address current_node = ranked_nodes[j];
                    ranked_nodes[j] = ranked_nodes[j + 1];
                    ranked_nodes[j + 1] = current_node;
                }   
            }    
        }
        return ranked_nodes;
    }

    function purchase_vouchToken() public payable setVouchTokenVerification(msg.sender){
        address trans_maker = msg.sender;
        Init_vouchToken(trans_maker);

    }

    function purchase_vouchToken_Test(address _node) public {
        Init_vouchToken(_node);
    }

    function delete_node(address _targetnode) public {

         //Outbound update from target node (Target_node --> Node A)
        uint len = vouchedList[_targetnode].vouchedToList.length;
        for(uint i = 0; i < len ; i ++){
            address out_targetnode = vouchedList[_targetnode].vouchedToList[i];
            vouchedList[out_targetnode].vouchedBy[_targetnode] = false;
            //Update inbound link array which target node vouch to
            uint len_inlink = vouchedList[out_targetnode].vouchedByList.length;
            for(uint j = 0; j < len_inlink; j++){
                if(vouchedList[out_targetnode].vouchedByList[j] == _targetnode){
                    delete vouchedList[out_targetnode].vouchedByList[j];
                }
            }
            //Update inbound count parameter of node that target node vouch to
            vouchedList[out_targetnode].total_inbound_link -= 1;
            //Check if node must be delete out from network
            if(vouchedList[out_targetnode].total_inbound_link == 0 && vouchedList[out_targetnode].total_outbound_link == 0){
                //nodes.pop(_unvouchTo);
                uint len_nodes = nodes.length;
                for(uint k = 0; k < len_nodes ; k ++){
                    if(nodes[k] == out_targetnode){
                        delete nodes[k];
                    }
                }
                vouchedList[out_targetnode].isAdded = false;
            }
        }
        //Inbound update from target node (Node A --> Target_node)
        uint len_to = vouchedList[_targetnode].vouchedByList.length;
        for(uint a = 0; a < len_to; a++){
           address in_targetnode = vouchedList[_targetnode].vouchedByList[a];
           vouchedList[in_targetnode].vouchedTo[_targetnode] = false;
           //Update outbound link array which vouch to target node
           uint lem_outlink = vouchedList[in_targetnode].vouchedToList.length;
           for(uint b = 0; b < lem_outlink; b++){
                if(vouchedList[in_targetnode].vouchedToList[b] == _targetnode){
                    delete vouchedList[in_targetnode].vouchedToList[b];
                }
            }
            //Update inbound count parameter of node that target node vouch to
            vouchedList[in_targetnode].total_outbound_link -= 1;
            if(vouchedList[in_targetnode].total_inbound_link == 0 && vouchedList[in_targetnode].total_outbound_link == 0){
                //nodes.pop(_unvouchTo);
                uint len_nodes2 = nodes.length;
                for(uint c = 0; c < len_nodes2 ; c ++){
                    if(nodes[c] == in_targetnode){
                        delete nodes[c];
                    }
                }
                vouchedList[in_targetnode].isAdded = false;
            }else{
                punlishment_list.push(in_targetnode);
            }
        }
        //Applied penalty of node in penalty list
        uint n = getNodesCount();
        uint penalty_len = punlishment_list.length;
        for(uint f = 0; f < penalty_len; f++) {
            address temp = punlishment_list[f];
            nodes_punishment(temp,n);
            delete punlishment_list[f];
        }
        

    }


    function makeVouch(address _vouchTo) public VouchVerification(_vouchTo){
        
        //Flag to vouched (Check vouch once)
        vouchedList[_vouchTo].isVouched = true;
        //Store inbound/outbount link to vouched/voucher account node
        vouchedList[_vouchTo].vouchedBy[msg.sender] = true;
        vouchedList[_vouchTo].vouchedByList.push(msg.sender);
        //Store outbount/inbound link to voucher/vouched account node
        vouchedList[msg.sender].vouchedTo[_vouchTo] = true;
        vouchedList[msg.sender].vouchedToList.push(_vouchTo);
        //Store count for inbound and out bound link
        vouchedList[_vouchTo].total_inbound_link += 1;
        vouchedList[msg.sender].total_outbound_link += 1;
        // total_inbound_link[_vouchTo] += 1;
        // total_outbound_link[msg.sender] += 1;

        //Store nodes in network
        addNodes(_vouchTo);
        addNodes(msg.sender);
        //To verified node in network
        vouchedList[_vouchTo].isAdded = true;
        vouchedList[msg.sender].isAdded = true;
        //calculate pagerank
        PagerankCal(nodes,getNodesCount());
        emit VouchLog(block.timestamp, msg.sender, _vouchTo);

    }

    //Remove edge out (Unvouch to account)
    function unvouched(address _unvouchTo) public UnvouchVerification(_unvouchTo){

        //Flag to vouched (Check vouch once)
        vouchedList[_unvouchTo].isVouched = false;
        //Store inbound link to vouched account node
        vouchedList[_unvouchTo].vouchedBy[msg.sender] = false;
        //vouchedList[_unvouchTo].vouchedByList.pop(msg.sender);
        //Update array list of inbound link of unvouched node and outbound of unvoucher node
        uint len = vouchedList[_unvouchTo].vouchedByList.length;
        for(uint i = 0; i < len ; i ++){
            if(vouchedList[_unvouchTo].vouchedByList[i] == msg.sender){
                delete vouchedList[_unvouchTo].vouchedByList[i];
            }
        }
        uint len_to = vouchedList[msg.sender].vouchedToList.length;
        for(uint j = 0; j < len_to ; j ++){
            if(vouchedList[msg.sender].vouchedToList[j] == _unvouchTo){
                delete vouchedList[msg.sender].vouchedToList[j];
            }
        }
        //Store outbount link to voucher account node
        vouchedList[msg.sender].vouchedTo[_unvouchTo] = false;
        //Store count for inbound and out bound link
        vouchedList[_unvouchTo].total_inbound_link -= 1;
        vouchedList[msg.sender].total_outbound_link -= 1;
        // total_inbound_link[_vouchTo] += 1;
        // total_outbound_link[msg.sender] += 1;

        if(vouchedList[_unvouchTo].total_inbound_link == 0 && vouchedList[_unvouchTo].total_outbound_link == 0){
            //nodes.pop(_unvouchTo);
            uint len_nodes = nodes.length;
            for(uint i = 0; i < len_nodes ; i ++){
                if(nodes[i] == _unvouchTo){
                    delete nodes[i];
                }
            }
            vouchedList[_unvouchTo].isAdded = false;
        }
        //calculate pagerank
        PagerankCal(nodes,getNodesCount());

    }

    // Add node into network
    function addNodes(address _node) internal {

        if(vouchedList[_node].isAdded == false) {
            nodes.push(_node);
        }
    }

    //Get number of all node in the network
    // function getNodesCount() internal view returns(uint){
    //     uint count;
    //     count = nodes.length; // n variables
    //     return count;
    // }
     //Get number of all node in the network
    function getNodesCount() public view returns(uint){
        uint count;
        count = nodes.length; // n variables
        return count;
    }

    function get_scores(address _node) public view returns(uint) {
        return vouchedList[_node].prScore;
    }

}

