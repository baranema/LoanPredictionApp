import re
from typing import Optional

from pydantic import BaseModel, Field, validator

from prediction.mappings import GRADES_MAPPING, SUB_GRADE_MAPPING

EMP_LENGTH_MAPPING = {
    "< 1 year": 0,
    "1 year": 1,
    "2 years": 2,
    "3 years": 3,
    "4 years": 4,
    "5 years": 5,
    "6 years": 6,
    "7 years": 7,
    "8 years": 8,
    "9 years": 9,
    "10+ years": 10,
}

PURPOSE_MAPPING = {
    "debt_consolidation": "debt consolid",
    "small_business": "small busi",
    "home_improvement": "home improv",
    "major_purchase": "major purchas",
    "credit_card": "credit card",
    "other": "other",
    "house": "hous",
    "vacation": "vacat",
    "car": "car",
    "medical": "medic",
    "moving": "move",
    "renewable_energy": "renew energi",
    "wedding": "wed",
    "educational": "educ",
}

TERM_MAPPING = {"60 months": 60, "36 months": 36}


class LoanStep1(BaseModel):
    """
    loan_amnt float64
    dti float64
    emp_length float64
    purpose object
    """

    loan_amnt: Optional[float] = Field(2500.0, ge=1)
    dti: float = Field(0.308, ge=0)
    emp_length: str = "5 years"
    purpose: str = "other"

    @validator("emp_length")
    def emp_length_must_have_value(cls, value):
        if value not in EMP_LENGTH_MAPPING.keys():
            if value.isnumeric():
                value = int(value)
            elif re.match(r"^-?\d+(?:\.\d+)$", value):
                value = int(float(value))

            if value not in EMP_LENGTH_MAPPING.values():
                raise ValueError(
                    f"expected emp_length values are {list(EMP_LENGTH_MAPPING.keys())}. Received value - {value}"
                )

        return value

    @validator("purpose")
    def purpose_must_have_value(cls, value):
        if (
            value not in PURPOSE_MAPPING.keys()
            and value not in PURPOSE_MAPPING.values()
        ):
            raise ValueError(
                f"expected purpose values are {list(PURPOSE_MAPPING.keys())}. Received value - {value}"
            )
        return value

    def get_entry_dict(self):
        data = {}
        data["loan_amnt"] = [self.loan_amnt]
        data["dti"] = [self.dti]

        if self.emp_length not in EMP_LENGTH_MAPPING.values():
            data["emp_length"] = [EMP_LENGTH_MAPPING[self.emp_length]]
        else:
            data["emp_length"] = [self.emp_length]

        if self.purpose not in PURPOSE_MAPPING.values():
            data["purpose"] = [PURPOSE_MAPPING[self.purpose]]
        else:
            data["purpose"] = [self.purpose]

        return data


class LoanStep2(BaseModel):
    sec_app_fico_range_low: float = 660.0
    verification_status: str = "Not Verified"
    sec_app_fico_range_high: float = 664.0
    percent_bc_gt_75: Optional[float] = Field(0.0, ge=0)
    open_rv_12m: Optional[float] = Field(5.0, ge=0)
    bc_util: Optional[float] = Field(23.2, ge=0)
    loan_amnt: Optional[float] = Field(28000.0, ge=1)
    fico_range_low: Optional[float] = Field(680.0, ge=0)
    pct_tl_nvr_dlq: Optional[float] = Field(95.2, ge=0)
    term: Optional[float] = Field(60, ge=0)
    num_rev_accts: Optional[float] = Field(17.0, ge=0)
    num_bc_tl: Optional[float] = Field(9.0, ge=0)
    inq_last_12m: Optional[float] = Field(2.0, ge=0)
    verification_status_joint: str = "Not Verified"
    mo_sin_rcnt_tl: Optional[float] = Field(3.0, ge=0)
    fico_range_high: Optional[float] = Field(684.0, ge=0)
    sec_app_num_rev_accts: float = 20.0
    total_bc_limit: Optional[float] = Field(5500.0, ge=0)
    bc_open_to_buy: Optional[float] = Field(4226.0, ge=0)
    num_tl_op_past_12m: Optional[float] = Field(7.0, ge=0)
    all_util: Optional[float] = Field(75.0, ge=0)
    open_rv_24m: Optional[float] = Field(6.0, ge=0)
    mo_sin_rcnt_rev_tl_op: Optional[float] = Field(6.0, ge=0)
    acc_open_past_24mths: Optional[float] = Field(8.0, ge=0)
    inq_fi: Optional[float] = Field(0.0, ge=0)
    purpose: str = "debt_consolidation"
    total_bal_ex_mort: Optional[float] = Field(55767.0, ge=0)
    total_rev_hi_lim: Optional[float] = Field(14700.0, ge=0)
    num_il_tl: Optional[float] = Field(6.0, ge=0)

    @validator("term")
    def term_must_have_value(cls, value):
        if value not in TERM_MAPPING.keys() and value not in TERM_MAPPING.values():
            raise ValueError(
                f"expected term values are {list(TERM_MAPPING.keys())}. Received value - {value}"
            )
        return value

    @validator("verification_status")
    def verification_status_must_have_value(cls, value):
        expected_status = ["Not Verified", "Source Verified", "Verified"]
        if value not in expected_status:
            raise ValueError(
                f"expected verification_status values are {expected_status}. Received value - {value}"
            )
        return value

    @validator("verification_status_joint")
    def verification_status_joint_must_have_value(cls, value):
        expected_status = [
            "Not Verified",
            "Source Verified",
            "Verified",
            "missing",
            "nan",
        ]
        if value not in expected_status:
            raise ValueError(
                f"expected verification_status values are {expected_status}. Received value - {value}"
            )
        return value

    @validator("purpose")
    def purpose_must_have_value(cls, value):
        if (
            value not in PURPOSE_MAPPING.keys()
            and value not in PURPOSE_MAPPING.values()
        ):
            raise ValueError(
                f"expected purpose values are {list(PURPOSE_MAPPING.keys())}. Received value - {value}"
            )
        return value

    @validator("sec_app_fico_range_high")
    def sec_app_fico_range_high_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected sec_app_fico_range_high values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected sec_app_fico_range_high value is 'nan' or numeric value."
            )
        return value

    @validator("sec_app_num_rev_accts")
    def sec_app_num_rev_accts_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected sec_app_num_rev_accts values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected sec_app_num_rev_accts value is 'nan' or numeric value."
            )
        return value

    @validator("sec_app_fico_range_low")
    def sec_app_fico_range_low_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected sec_app_fico_range_low values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected sec_app_fico_range_low value is 'nan' or numeric value."
            )
        return value

    def get_entry_dict(self):
        data = {}
        for col, val in vars(self).items():
            if col == "purpose":
                if val not in PURPOSE_MAPPING.values():
                    data["purpose"] = [PURPOSE_MAPPING[self.purpose]]
                else:
                    data["purpose"] = [self.purpose]
            elif col == "term":
                if val not in TERM_MAPPING.values():
                    data["term"] = [TERM_MAPPING[self.term]]
                else:
                    data["term"] = [self.term]
            else:
                data[col] = [val]

        return data


class LoanStep3(BaseModel):
    open_rv_12m: Optional[float] = Field(8.0, ge=0)
    mo_sin_rcnt_tl: Optional[float] = Field(3.0, ge=0)
    annual_inc: Optional[float] = Field(76600.0, ge=0)
    sec_app_fico_range_high: Optional[float] = Field(654.0, ge=0)
    sec_app_fico_range_low: float = 650.0
    verification_status_joint: str = "Not Verified"
    bc_open_to_buy: Optional[float] = Field(15507.0, ge=0)
    purpose: str = "debt_consolidation"
    mort_acc: Optional[float] = Field(0.0, ge=0)
    loan_amnt: Optional[float] = Field(20000.0, ge=1)
    inq_fi: Optional[float] = Field(8.0, ge=0)
    emp_length: Optional[float] = Field(0, ge=0)
    fico_range_low: Optional[float] = Field(675.0, ge=0)
    bc_util: Optional[float] = Field(45.0, ge=0)
    num_rev_accts: Optional[float] = Field(45.0, ge=0)
    acc_open_past_24mths: Optional[float] = Field(22.0, ge=0)
    pct_tl_nvr_dlq: Optional[float] = Field(84.5, ge=0)
    mo_sin_old_il_acct: Optional[float] = Field(122.0, ge=0)
    fico_range_high: Optional[float] = Field(679.0, ge=0)
    grade: Optional[float] = Field(6, ge=0)
    sec_app_num_rev_accts: float = 25.0
    mths_since_recent_revol_delinq: Optional[float] = Field(62.0, ge=0)
    max_bal_bc: Optional[float] = Field(6567.0, ge=0)
    mo_sin_rcnt_rev_tl_op: Optional[float] = Field(3.0, ge=0)
    annual_inc_joint: float = 109888.0
    num_rev_tl_bal_gt_0: Optional[float] = Field(11.0, ge=0)
    total_bc_limit: Optional[float] = Field(28200.0, ge=0)
    term: Optional[float] = Field(60, ge=0)
    num_sats: Optional[float] = Field(35.0, ge=0)
    num_tl_op_past_12m: Optional[float] = Field(9.0, ge=0)
    total_rev_hi_lim: Optional[float] = Field(53600.0, ge=0)
    home_ownership: str = "RENT"
    inq_last_12m: Optional[float] = Field(15.0, ge=0)
    sec_app_mort_acc: float = 0.0
    all_util: Optional[float] = Field(37.0, ge=0)
    verification_status: str = "Verified"
    percent_bc_gt_75: Optional[float] = Field(14.3, ge=0)

    @validator("sec_app_num_rev_accts")
    def sec_app_num_rev_accts_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected sec_app_num_rev_accts values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected sec_app_num_rev_accts value is 'nan' or numeric value."
            )
        return value

    @validator("sec_app_fico_range_low")
    def sec_app_fico_range_low_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected sec_app_fico_range_low values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected sec_app_fico_range_low value is 'nan' or numeric value."
            )
        return value

    @validator("sec_app_fico_range_high")
    def sec_app_fico_range_high_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected sec_app_fico_range_high values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected sec_app_fico_range_high value is 'nan' or numeric value."
            )
        return value

    @validator("sec_app_mort_acc")
    def sec_app_mort_acc_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected sec_app_mort_acc values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected sec_app_mort_acc value is 'nan' or numeric value."
            )
        return value

    @validator("verification_status")
    def verification_status_must_have_value(cls, value):
        expected_status = ["Not Verified", "Source Verified", "Verified"]
        if value not in expected_status:
            raise ValueError(
                f"expected verification_status values are {expected_status}. Received value - {value}"
            )
        return value

    @validator("verification_status_joint")
    def verification_status_joint_must_have_value(cls, value):
        expected_status = [
            "Not Verified",
            "Source Verified",
            "Verified",
            "missing",
            "nan",
        ]
        if value not in expected_status:
            raise ValueError(
                f"expected verification_status values are {expected_status}. Received value - {value}"
            )
        return value

    @validator("purpose")
    def purpose_must_have_value(cls, value):
        if (
            value not in PURPOSE_MAPPING.keys()
            and value not in PURPOSE_MAPPING.values()
        ):
            raise ValueError(
                f"expected purpose values are {list(PURPOSE_MAPPING.keys())}. Received value - {value}"
            )
        return value

    @validator("annual_inc_joint")
    def annual_inc_joint_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected annual_inc_joint values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected annual_inc_joint value is 'nan' or numeric value."
            )
        return value

    def get_entry_dict(self):
        data = {}
        for col, val in vars(self).items():
            if col == "purpose":
                if val not in PURPOSE_MAPPING.values():
                    data["purpose"] = [PURPOSE_MAPPING[self.purpose]]
                else:
                    data["purpose"] = [self.purpose]
            else:
                data[col] = [val]

        return data


class LoanStep4(BaseModel):
    loan_amnt: Optional[float] = Field(16000.0, ge=1)
    term: Optional[float] = Field(60, ge=0)
    grade: str = "B"
    sub_grade: str = "B4"
    home_ownership: str = "MORTGAGE"
    annual_inc: Optional[float] = Field(57000.0, ge=0)
    verification_status: str = "Not Verified"
    purpose: str = "credit_card"
    dti: Optional[float] = Field(13.68, ge=0)
    fico_range_low: Optional[float] = Field(705.0, ge=0)
    fico_range_high: Optional[float] = Field(709.0, ge=0)
    open_acc: Optional[float] = Field(19.0, ge=0)
    revol_bal: Optional[float] = Field(2777.0, ge=0)
    application_type: str = "Joint App"
    annual_inc_joint: float = 89000.0
    dti_joint: float = 10.8
    verification_status_joint: str = "Not Verified"
    open_rv_12m: Optional[float] = Field(0.0, ge=0)
    open_rv_24m: Optional[float] = Field(0.0, ge=0)
    all_util: Optional[float] = Field(91.0, ge=0)
    total_rev_hi_lim: Optional[float] = Field(26000.0, ge=0)
    inq_fi: Optional[float] = Field(1.0, ge=0)
    inq_last_12m: Optional[float] = Field(3.0, ge=0)
    acc_open_past_24mths: Optional[float] = Field(3.0, ge=0)
    bc_open_to_buy: Optional[float] = Field(14223.0, ge=0)
    bc_util: Optional[float] = Field(16.3, ge=0)
    mo_sin_old_rev_tl_op: Optional[float] = Field(317.0, ge=0)
    mo_sin_rcnt_rev_tl_op: Optional[float] = Field(45.0, ge=0)
    mo_sin_rcnt_tl: Optional[float] = Field(9.0, ge=0)
    mort_acc: Optional[float] = Field(3.0, ge=0)
    num_rev_accts: Optional[float] = Field(8.0, ge=0)
    num_tl_op_past_12m: Optional[float] = Field(2.0, ge=0)
    percent_bc_gt_75: Optional[float] = Field(50.0, ge=0)
    total_bc_limit: Optional[float] = Field(17000.0, ge=0)
    revol_bal_joint: float = 11766.0
    sec_app_fico_range_low: float = 680.0
    sec_app_fico_range_high: float = 684.0
    sec_app_mort_acc: float = 3.0
    sec_app_open_acc: float = 6.0
    sec_app_num_rev_accts: float = 7.0

    @validator("sec_app_open_acc")
    def sec_app_open_acc_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected sec_app_open_acc values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected sec_app_open_acc value is 'nan' or numeric value."
            )
        return value

    @validator("sec_app_num_rev_accts")
    def sec_app_num_rev_accts_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected sec_app_num_rev_accts values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected sec_app_num_rev_accts value is 'nan' or numeric value."
            )
        return value

    @validator("sec_app_fico_range_low")
    def sec_app_fico_range_low_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected sec_app_fico_range_low values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected sec_app_fico_range_low value is 'nan' or numeric value."
            )
        return value

    @validator("sec_app_fico_range_high")
    def sec_app_fico_range_high_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected sec_app_fico_range_high values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected sec_app_fico_range_high value is 'nan' or numeric value."
            )
        return value

    @validator("sec_app_mort_acc")
    def sec_app_mort_acc_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected sec_app_mort_acc values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected sec_app_mort_acc value is 'nan' or numeric value."
            )
        return value

    @validator("term")
    def term_must_have_value(cls, value):
        if value not in TERM_MAPPING.keys() and value not in TERM_MAPPING.values():
            raise ValueError(
                f"expected term values are {list(TERM_MAPPING.keys())}. Received value - {value}"
            )
        return value

    @validator("purpose")
    def purpose_must_have_value(cls, value):
        if value not in PURPOSE_MAPPING.keys():
            raise ValueError(
                f"expected purpose values are {list(PURPOSE_MAPPING.keys())}. Received value - {value}"
            )
        return value

    @validator("revol_bal_joint")
    def revol_bal_joint_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected revol_bal_joint values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected revol_bal_joint value is 'nan' or numeric value."
            )
        return value

    @validator("annual_inc_joint")
    def annual_inc_joint_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError(
                    "expected annual_inc_joint values must be greater than 0."
                )
        elif value != "nan":
            raise ValueError(
                "expected annual_inc_joint value is 'nan' or numeric value."
            )
        return value

    @validator("dti_joint")
    def dti_joint_joint_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError("expected dti_joint values must be greater than 0.")
        elif value != "nan":
            raise ValueError("expected dti_joint value is 'nan' or numeric value.")
        return value

    @validator("verification_status")
    def verification_status_must_have_value(cls, value):
        expected_status = ["Not Verified", "Source Verified", "Verified"]
        if value not in expected_status:
            raise ValueError(
                f"expected verification_status values are {expected_status}. Received value - {value}"
            )
        return value

    @validator("verification_status_joint")
    def verification_status_joint_must_have_value(cls, value):
        expected_status = [
            "Not Verified",
            "Source Verified",
            "Verified",
            "missing",
            "nan",
        ]
        if value not in expected_status:
            raise ValueError(
                f"expected verification_status values are {expected_status}. Received value - {value}"
            )
        return value

    @validator("grade")
    def grade_must_have_value(cls, value):
        if value not in GRADES_MAPPING.values():
            raise ValueError(
                f"expected grade values are {GRADES_MAPPING.values()}. Received value - {value}"
            )
        return value

    @validator("sub_grade")
    def sub_grade_must_have_value(cls, value):
        if value not in SUB_GRADE_MAPPING.values():
            raise ValueError(
                f"expected sub_grade values are {SUB_GRADE_MAPPING.values()}. Received value - {value}"
            )
        return value

    @validator("application_type")
    def application_type_must_have_value(value):
        expected = ["Joint App", "Individual"]
        if value not in expected:
            raise ValueError(
                f"expected application_type values are {expected}. Received value - {value}"
            )
        return value

    @validator("home_ownership")
    def home_ownership_must_have_value(value):
        expected = ["MORTGAGE", "RENT", "OWN", "NONE", "ANY", "OTHER"]
        if value not in expected:
            raise ValueError(
                f"expected home_ownership values are {expected}. Received value - {value}"
            )
        return value

    def get_entry_dict(self):
        data = {}
        for col, val in vars(self).items():
            if col == "term":
                if val not in TERM_MAPPING.values():
                    data["term"] = [TERM_MAPPING[self.term]]
                else:
                    data["term"] = [self.term]
            else:
                data[col] = [val]

        return data
