// SPDX-License-Identifier: MIT

pragma solidity >=0.8.0;

contract PartnerAgreement {
    address payable _owner;
    uint256 effectiveDate;

    string companyName;
    string companyLicenseNumber;
    string partnerName;
    string partnerEmail;
    Bank partnerBank;
    RebatePlan rebatePlan;

    constructor() {
        _owner = payable(msg.sender);
    }

    struct Bank {
        string name;
        string accountNumber;
        string branchName;
        string swiftCode;
    }

    struct RebatePlan {
        // Product name to the corresponding rebate schedule
        mapping(string => RebateSchedule1) lotBasedRebateSchedule;
        mapping(string => RebateSchedule2) amountBasedRebateSchedule;
    }

    struct RebateSchedule1 {
        string condition;
        uint8 value;
    }

    struct RebateSchedule2 {
        /* +Pip or fixed amount
         * type_ = 0: +Pip; type_ = 1: fixed amount
         */
        uint8 type_;
        uint256 value;
    }

    modifier onlyOwner() {
        // require(msg.sender == _owner, "You are not the owner.");
        _;
    }

    mapping(string => uint256) public nameToPartner;

    function setEffectiveDate(uint256 _effectiveDate) public onlyOwner {
        effectiveDate = _effectiveDate;
    }

    function setBankName(string memory _name) public {
        partnerBank.name = _name;
    }

    function getBankName() public view onlyOwner returns (string memory) {
        return partnerBank.name;
    }

    function addLotBasedRebateSchedule(
        string memory _productName,
        string memory _condition,
        uint8 _value
    ) public {
        rebatePlan.lotBasedRebateSchedule[_productName] = RebateSchedule1(
            _condition,
            _value
        );
    }

    function addAmountBasedRebateSchedule(
        string memory _productName,
        uint8 _type_,
        uint256 _value
    ) public {
        rebatePlan.amountBasedRebateSchedule[_productName] = RebateSchedule2(
            _type_,
            _value
        );
    }

    function destroySmartContract() public onlyOwner {
        selfdestruct(_owner);
    }
}
