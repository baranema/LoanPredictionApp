from typing import Optional
from pydantic import Field, BaseModel, validator

EMP_LENGTH_MAPPING = {
    '< 1 year': 0,
    '1 year': 1,
    '2 years': 2,
    '3 years': 3,
    '4 years': 4,
    '5 years': 5,
    '6 years': 6,
    '7 years': 7,
    '8 years': 8, 
    '9 years': 9,
    '10+ years': 10
}

PURPOSE_MAPPING = {
    'debt_consolidation': 'debt consolid',
    'small_business': 'small busi',
    'home_improvement': 'home improv',
    'major_purchase': 'major purchas',
    'credit_card': 'credit card',
    'other': 'other', 
    'house': 'hous', 
    'vacation': 'vacat',
    'car': 'car', 
    'medical': 'medic', 
    'moving': 'move',
    'renewable_energy': 'renew energi',
    'wedding': 'wed',
    'educational': 'educ'
}

TERM_MAPPING = {
    '60 months': 60,
    '36 months': 36
}

class LoanStep1(BaseModel):
    '''
        loan_amnt float64
        dti float64
        emp_length float64
        purpose object
    '''

    loan_amnt: Optional[float] = Field(2500.0, ge=1, le=10000000000)
    dti: float = Field(0.308, ge=0, le=10000000000)
    emp_length: str = "5 years"
    purpose: str = "other"
    
    @validator("emp_length")
    def emp_length_must_have_value(cls, value):
        if value not in EMP_LENGTH_MAPPING.keys() and value not in EMP_LENGTH_MAPPING.values(): 
            raise ValueError(f"expected emp_length values are {list(EMP_LENGTH_MAPPING.keys())}. Received value - {value}")
        
        return value
   
    @validator("purpose")
    def purpose_must_have_value(cls, value):
        if value not in PURPOSE_MAPPING.keys() and value not in PURPOSE_MAPPING.values():
            raise ValueError(f"expected purpose values are {list(PURPOSE_MAPPING.keys())}. Received value - {value}")
        return value
   
    def get_entry_dict(self):
        data = {} 
        data["loan_amnt"] = [self.loan_amnt]
        data["dti"] = [self.dti]

        if self.emp_length not in EMP_LENGTH_MAPPING.values():
            data["emp_length"] = [EMP_LENGTH_MAPPING[self.emp_length]]
        else:
            data["emp_length"] = self.emp_length
      
        if self.purpose not in PURPOSE_MAPPING.values():
            data["purpose"] = [PURPOSE_MAPPING[self.purpose]]
        else:
            data["purpose"] = self.purpose
        
        return data

    
class LoanStep2(BaseModel):
    open_acc: Optional[float] = Field(4.0, ge=1, le=10**10)
    loan_amnt: Optional[float] = Field(5000.0, ge=1, le=10**10)
    sec_app_fico_range_low: Optional[float] = Field(565.0, ge=1, le=10**10)
    annual_inc_joint: Optional[float] = Field(77500.0, ge=1, le=10**10)
    mo_sin_old_rev_tl_op: Optional[float] = Field(100.0, ge=1, le=10**10)
    bc_util: Optional[float] = Field(13.4, ge=1, le=10**10)
    total_rev_hi_lim: Optional[float] = Field(8700.0, ge=1, le=10**10)
    tot_hi_cred_lim: Optional[float] = Field(35519.0, ge=1, le=10**10)
    inq_last_12m: Optional[float] = Field(1.0, ge=1, le=10**10)
    verification_status_joint: str = "Not Verified"
    purpose: str = "debt_consolidation"
    total_bc_limit: Optional[float] = Field(7200.0, ge=1, le=10**10)
    fico_range_low: Optional[float] = Field(715.0, ge=1, le=10**10)
    open_rv_24m: Optional[float] = Field(4.0, ge=1, le=10**10)
    mo_sin_rcnt_rev_tl_op: Optional[float] = Field(1.0, ge=1, le=10**10)
    num_bc_sats: Optional[float] = Field(2.0, ge=1, le=10**10)
    all_util: Optional[float] = Field(78.0, ge=1, le=10**10)
    sec_app_fico_range_high: Optional[float] = Field(569.0, ge=1, le=10**10)
    num_tl_op_past_12m: Optional[float] = Field(2.0, ge=1, le=10**10)
    acc_open_past_24mths: Optional[float] = Field(5.0, ge=1, le=10**10)
    bc_open_to_buy: Optional[float] = Field(6233.0, ge=1, le=10**10)
    verification_status: str = "Not Verified"
    sec_app_open_acc: Optional[float] = Field(7.0, ge=1, le=10**10)
    pct_tl_nvr_dlq: Optional[float] = Field(83.3, ge=1, le=10**10)
    fico_range_high: Optional[float] = Field(719.0, ge=1, le=10**10)
    num_actv_rev_tl: Optional[float] = Field(2.0, ge=1, le=10**10)
    open_rv_12m: Optional[float] = Field(1.0, ge=1, le=10**10)
    percent_bc_gt_75: Optional[float] = Field(0.0, ge=1, le=10**10)
    mo_sin_rcnt_tl: Optional[float] = Field(1.0, ge=1, le=10**10)
    inq_fi: Optional[float] = Field(0.0, ge=1, le=10**10)
    annual_inc: Optional[float] = Field(33000.0, ge=1, le=10**10)

    # @validator("term")
    # def term_must_have_value(cls, value):
    #     if value not in TERM_MAPPING.keys():
    #         raise ValueError(f"expected term values are {list(TERM_MAPPING.keys())}. Received value - {value}")
    #     return value
    
    # @validator("verification_status")
    # @validator("verification_status_joint")
    # def verification_status_must_have_value(cls, value):
    #     expected_status = ['Not Verified' 'Source Verified' 'Verified']
    #     if value not in expected_status:
    #         raise ValueError(f"expected verification_status values are {expected_status}. Received value - {value}")
    #     return value
        
    # @validator("purpose")
    # def purpose_must_have_value(cls, value):
    #     print(len(['debt_consolidation' 'other' 'credit_card' 'home_improvement' 'medical'
    #         'vacation' 'renewable_energy' 'small_business' 'car' 'moving' 'house'
    #         'major_purchase' 'wedding']))
    #     print(len(list(PURPOSE_MAPPING.keys())))

    #     if value not in PURPOSE_MAPPING.keys():
    #         raise ValueError(f"expected purpose values are {list(PURPOSE_MAPPING.keys())}. Received value - {value}")
    #     return value