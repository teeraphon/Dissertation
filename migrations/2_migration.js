var Vouch = artifacts.require("Vouch");

module.exports = function (deployer) {
  // deployment steps
  deployer.deploy(Vouch);
};
