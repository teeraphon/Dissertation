const Vouch = artifacts.require(
  "/Users/teera/Desktop/Dissertation/contracts/reputation_backup160822.sol"
);

contract("Vouch", (accounts) => {
  it("Requirement A : Make vouch", async () => {
    // Get test account A and B
    const node_A = accounts[0];
    const node_B = accounts[1];
    // Set token price
    const price = web3.utils.toWei("1", "ether");
    // Retreive contract
    const contract = await Vouch.deployed();
    // Purchasing vouch token
    await contract.purchase_vouchToken({ from: node_A, value: price });
    // Get current vouch token on node A
    const nodeA_details = await contract.vouchedList(node_A);
    assert.equal(nodeA_details.vouch_token, 100, "Vouch token must set to 100");
    // Start to make vouch
    await contract.makeVouch(node_B, { from: node_A });
    // Parameter verification to ensure that vouch is complete
    const nodeB_details = await contract.vouchedList(node_B);
    // Node B parameter verification

    assert.equal(
      nodeB_details.total_outbound_link,
      0,
      "Node B who recieve vouch must have outbound link = 0"
    );
    assert.equal(
      nodeB_details.total_inbound_link,
      1,
      "Node B who recieve vouch must have inbound link = 1"
    );

    // Verified rank score
    assert.equal(
      nodeA_details.prScore < nodeB_details.prScore,
      true,
      "Pagerank socre of node A must less than node B"
    );
  });

  it("Requirement B : Vouch detaching", async () => {
    // Get test account A and B
    const node_A = accounts[2];
    const node_B = accounts[3];
    const price = web3.utils.toWei("1", "ether");
    // Retreive contract
    const contract = await Vouch.deployed();
    // Purchasing vouch token
    await contract.purchase_vouchToken({ from: node_A, value: price });
    await contract.purchase_vouchToken({ from: node_B, value: price });
    // Make vouch
    await contract.makeVouch(node_B, { from: node_A });
    await contract.makeVouch(node_A, { from: node_B });
    // Vouch detaching
    await contract.unvouched(node_A, { from: node_B });
    // Verified Pagerank score
    const nodeA_details = await contract.vouchedList(node_A);
    const nodeB_details = await contract.vouchedList(node_B);
    // Verified Pagerank score
    assert.equal(
      nodeA_details.prScore < nodeB_details.prScore,
      true,
      "Pagerank score of node A must less than node B"
    );
  });

  it("Requirement C : Node deletion", async () => {
    // Get test account A and B and C
    const node_A = accounts[2];
    const node_B = accounts[3];
    const node_C = accounts[4];
    // Set token price
    const price = web3.utils.toWei("1", "ether");
    // Init deployed contract
    const contract = await Vouch.deployed();
    await contract.makeVouch(node_C, { from: node_B });
    // Get pervious vouch token of B
    let previous_token = await contract.vouchedList(node_B).vouch_token;
    // Node C deletion
    await contract.delete_node(node_C, { from: node_A });
    // Start to check parameter
    const nodeB_details = await contract.vouchedList(node_B);
    // Verified parameter
    assert.equal(
      nodeB_details.total_outbound_link,
      0,
      "Edges between node B and C must be removed"
    );
    // Verified penalties
    // console.log(parseInt(previous_token));
    // console.log(parseInt(nodeB_details.vouch_token));
    // Verified token reduction
    assert.equal(
      nodeB_details.vouch_token < 100,
      true,
      "Vouch token of node B must be reduced"
    );
  });

  it("Requirement D : Pagerank calculation", async () => {
    // Get test account A and B
    const node_A = accounts[0];
    const node_B = accounts[1];
    // Init deployed contract
    const contract = await Vouch.deployed();
    // Get current vouch token on node A
    const nodeA_details = await contract.vouchedList(node_A);
    // Parameter verification to ensure that vouch is complete
    const nodeB_details = await contract.vouchedList(node_B);
    // Node B parameter verification

    assert.equal(
      nodeB_details.total_outbound_link,
      0,
      "Node B who recieve vouch must have outbound link = 0"
    );
    assert.equal(
      nodeB_details.total_inbound_link,
      1,
      "Node B who recieve vouch must have inbound link = 1"
    );

    // Verified rank score
    assert.equal(
      nodeA_details.prScore < nodeB_details.prScore,
      true,
      "Pagerank socre of node A must less than node B"
    );
    assert.equal(
      nodeA_details.prScore,
      15,
      "Pagerank score of node A(Account 0) must equal to 15"
    );
    assert.equal(
      nodeB_details.prScore,
      27,
      "Pagerank score of node B(Account 1) must equal to 27"
    );
  });

  it("Requirement E : Node penalties", async () => {
    // Get test account A and B and C
    const node_B = accounts[3];
    // Init deployed contract
    const contract = await Vouch.deployed();
    // Start to check parameter
    const nodeB_details = await contract.vouchedList(node_B);
    // Verified parameter
    assert.equal(
      nodeB_details.total_outbound_link,
      0,
      "Edges between node B and C must be removed"
    );
    // Verified penalties
    // console.log(parseInt(previous_token));
    // console.log(parseInt(nodeB_details.vouch_token));
    // Verified token reduction
    assert.equal(
      nodeB_details.vouch_token,
      75,
      "Vouch token of node B must be 75"
    );
  });
});
