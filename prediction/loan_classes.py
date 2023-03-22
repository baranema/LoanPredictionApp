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

PURPOSE_VALUES = {
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

class LoanStep1(BaseModel):
    '''
        loan_amnt float64
        dti float64
        emp_length float64
        purpose object
    '''

    loan_amnt: Optional[float] = Field(2500.0, ge=1, le=10000000000)
    dti: float = 0.308
    emp_length: str = "5 years"
    purpose: str = "other"

    @validator("loan_amnt")
    def loan_amnt_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError(f"expected loan_amnt >= 0, received value - {value}")
        return value

    @validator("dti")
    def dti_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError(f"expected dti >= 0, received value - {value}")
        return value

    @validator("emp_length")
    def emp_length_must_have_value(cls, value):
        if value not in EMP_LENGTH_MAPPING.keys():
            raise ValueError(f"expected emp_length values are {list(EMP_LENGTH_MAPPING.keys())}. Received value - {value}")
        return value
   
    @validator("purpose")
    def purpose_must_have_value(cls, value):
        if value not in PURPOSE_VALUES.keys():
            raise ValueError(f"expected purpose values are {list(PURPOSE_VALUES.keys())}. Received value - {value}")
        return value
   
    def get_entry_dict(self):
        data = {}

        data["loan_amnt"] = [self.loan_amnt]
        data["dti"] = [self.dti]
        data["emp_length"] = [EMP_LENGTH_MAPPING[self.emp_length]]
        data["purpose"] = [PURPOSE_VALUES[self.purpose]]
 
        return data

    
# class LoanStep2(BaseModel):
#     open_acc: float = 4.0
#     loan_amnt: float = 5000.0
#     sec_app_fico_range_low: float = 565.0
#     annual_inc_joint: float = 77500.0
#     mo_sin_old_rev_tl_op: float = 100.0
#     bc_util: float = 13.4
#     total_rev_hi_lim: float = 8700.0
#     tot_hi_cred_lim: float = 35519.0
#     term: int = 36
#     inq_last_12m: float = 1.0
#     verification_status_joint: str = "Not Verified"
#     purpose: str = "debt_consolidation"
#     total_bc_limit: float = 7200.0
#     fico_range_low: float = 715.0
#     open_rv_24m: float = 4.0
#     mo_sin_rcnt_rev_tl_op: float = 1.0
#     num_bc_sats: float = 2.0
#     all_util: float = 78.0
#     sec_app_fico_range_high: float = 569.0
#     num_tl_op_past_12m: float = 2.0
#     acc_open_past_24mths: float = 5.0
#     bc_open_to_buy: float = 6233.0
#     verification_status: str = "Not Verified"
#     sec_app_open_acc: float = 7.0
#     pct_tl_nvr_dlq: float = 83.3
#     fico_range_high: float = 719.0
#     num_actv_rev_tl: float = 2.0
#     open_rv_12m: float = 1.0
#     percent_bc_gt_75: float = 0.0
#     mo_sin_rcnt_tl: float = 1.0
#     inq_fi: float = 0.0
#     annual_inc: float = 33000.0
