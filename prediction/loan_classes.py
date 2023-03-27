import re
from typing import Optional

import pandas as pd
from pydantic import BaseModel, Field, validator

from prediction.mappings import GRADES_MAPPING, SUB_GRADE_MAPPING

# Dictionary for mapping employment length values to integers
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

# Dictionary for mapping loan purpose values to shorter strings
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

# Dictionary for mapping loan term values to integers
TERM_MAPPING = {"60 months": 60, "36 months": 36}


class LoanStep1(BaseModel):
    """
    Represents the first step in a loan application.
    """

    # The loan amount.
    loan_amnt: Optional[float] = Field(2500.0, ge=1)

    # The debt-to-income ratio.
    dti: float = Field(0.308, ge=0)

    # The length of employment in years.
    emp_length: str = "5 years"

    # The purpose of the loan.
    purpose: str = "other"

    # Ensure that emp_length is a valid value and convert to integer if necessary.
    @validator("emp_length")
    def emp_length_must_have_value(cls, value):
        if value not in EMP_LENGTH_MAPPING.keys():
            # If value is numeric or a float represented as a string, convert to integer.
            if value.isnumeric():
                value = int(value)
            elif re.match(r"^-?\d+(?:\.\d+)$", value):
                value = int(float(value))

            if value not in EMP_LENGTH_MAPPING.values():
                raise ValueError(
                    f"expected emp_length values are {list(EMP_LENGTH_MAPPING.keys())}. Received value - {value}"
                )

        return value

    # Ensure that purpose is a valid value.
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

    # Returns a dictionary representing the instance suitable for use in a machine learning model.
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
    bc_open_to_buy: Optional[float] = Field(12558.0, ge=0)
    fico_range_high: Optional[float] = Field(729.0, ge=0)
    num_tl_op_past_12m: Optional[float] = Field(5.0, ge=0)
    sec_app_mort_acc: float = 0.0
    revol_bal_joint: float = 17666.0
    all_util: Optional[float] = Field(48.0, ge=0)
    annual_inc: Optional[float] = Field(70000.0, ge=0)
    verification_status: str = "Verified"
    revol_bal: Optional[float] = Field(1322.0, ge=0)
    dti: Optional[float] = Field(10.34, ge=0)
    total_cu_tl: Optional[float] = Field(3.0, ge=0)
    dti_joint: float = 18.74
    mort_acc: Optional[float] = Field(5.0, ge=0)
    inq_last_12m: Optional[float] = Field(5.0, ge=0)
    max_bal_bc: Optional[float] = Field(942.0, ge=0)
    sec_app_fico_range_high: float = 674.0
    open_rv_12m: Optional[float] = Field(2.0, ge=0)
    num_tl_120dpd_2m: Optional[float] = Field(0.0, ge=0)
    percent_bc_gt_75: Optional[float] = Field(0.0, ge=0)
    inq_fi: Optional[float] = Field(0.0, ge=0)
    verification_status_joint: str = "Not Verified"
    annual_inc_joint: float = 94000.0
    sec_app_fico_range_low: float = 670.0
    fico_range_low: Optional[float] = Field(725.0, ge=0)
    term: Optional[int] = Field(60, ge=0)
    pct_tl_nvr_dlq: Optional[float] = Field(100.0, ge=0)
    open_rv_24m: Optional[float] = Field(2.0, ge=0)
    purpose: str = "other"
    loan_amnt: Optional[float] = Field(15000.0, ge=0)
    num_actv_bc_tl: Optional[float] = Field(1.0, ge=0)
    mo_sin_rcnt_tl: Optional[float] = Field(3.0, ge=0)
    acc_open_past_24mths: Optional[float] = Field(5.0, ge=0)
    fico_avg: Optional[float] = Field(727.0, ge=0)
    sec_app_fico_avg: float = 672.0
    fico_diff: Optional[float] = Field(4.0, ge=0)
    sec_app_fico_diff: float = 4.0
    loan_size_category: str = "10K - 20K"

    @property
    def loan_size_category(self):
        bins = [0, 5000, 10000, 20000, 30000, 40000, float("inf")]
        labels = ["< 5K", "5K - 10K", "10K - 20K", "20K - 30K", "30K - 40K", ">= 40K"]
        if self.loan_amnt is not None:
            return pd.cut([self.loan_amnt], bins=bins, labels=labels)[0]
        return None

    @property
    def fico_diff(self):
        if self.fico_range_high is not None and self.fico_range_low is not None:
            return self.fico_range_high - self.fico_range_low
        return None

    @property
    def sec_app_fico_diff(self):
        if (
            self.sec_app_fico_range_high is not None
            and self.sec_app_fico_range_low is not None
        ):
            return self.sec_app_fico_range_high - self.sec_app_fico_range_low
        return None

    @property
    def LTI(self):
        if self.annual_inc_joint is not None:
            return self.loan_amnt / self.annual_inc_joint
        elif self.annual_inc_joint is not None:
            return self.loan_amnt / self.annual_inc
        return None

    @property
    def sec_app_fico_avg(self):
        if self.sec_app_fico_range_low and self.sec_app_fico_range_high:
            return (self.sec_app_fico_range_high + self.sec_app_fico_range_low) / 2
        return None

    @property
    def fico_avg(self):
        if self.fico_range_low and self.fico_range_high:
            return (self.fico_range_high + self.fico_range_low) / 2
        return None

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

    @validator("dti_joint")
    def dti_joint_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError("expected dti_joint values must be greater than 0.")
        elif value != "nan":
            raise ValueError("expected dti_joint value is 'nan' or numeric value.")
        return value

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
            if col == "term":
                if val not in TERM_MAPPING.values():
                    data["term"] = [TERM_MAPPING[self.term]]
                else:
                    data["term"] = [self.term]
            else:
                data[col] = [val]

        if "sec_app_fico_avg" not in list(data.keys()):
            data["sec_app_fico_avg"] = [self.sec_app_fico_avg]

        if "fico_avg" not in list(data.keys()):
            data["fico_avg"] = [self.fico_avg]

        if "fico_diff" not in list(data.keys()):
            data["fico_diff"] = [self.fico_diff]
            
        if "loan_size_category" not in list(data.keys()):
            data["loan_size_category"] = [self.loan_size_category]

        if "sec_app_fico_diff" not in list(data.keys()):
            data["sec_app_fico_diff"] = [self.sec_app_fico_diff]

        return data


class LoanStep3(BaseModel):
    bc_open_to_buy: Optional[float] = Field(3440.0, ge=0)
    fico_range_high: Optional[float] = Field(689.0, ge=0)
    emp_length: Optional[float] = Field(0.0, ge=0)
    num_tl_op_past_12m: Optional[float] = Field(2.0, ge=0)
    sec_app_mort_acc: float = 2.0
    num_il_tl: Optional[float] = Field(4.0, ge=0)
    bc_util: Optional[float] = Field(36.3, ge=0)
    all_util: Optional[float] = Field(65.0, ge=0)
    annual_inc: Optional[float] = Field(60000.0, ge=0)
    verification_status: str = "Not Verified"
    dti: Optional[float] = Field(8.46, ge=0)
    total_rev_hi_lim: Optional[float] = Field(11500.0, ge=0)
    dti_joint: float = 9.19
    num_sats: Optional[float] = Field(9.0, ge=0)
    mort_acc: Optional[float] = Field(0.0, ge=0)
    inq_last_12m: Optional[float] = Field(1.0, ge=0)
    sec_app_fico_range_high: float = 644.0
    open_rv_12m: Optional[float] = Field(1.0, ge=0)
    verification_status_joint: str = "Not Verified"
    percent_bc_gt_75: Optional[float] = Field(0.0, ge=0)
    grade: str = "B"
    inq_fi: Optional[float] = Field(0.0, ge=0)
    annual_inc_joint: float = 96000.0
    mo_sin_old_rev_tl_op: Optional[float] = Field(24.0, ge=0)
    sec_app_fico_range_low: float = 640.0
    avg_cur_bal: Optional[float] = Field(1772.0, ge=0)
    fico_range_low: Optional[float] = Field(685.0, ge=0)
    term: Optional[int] = Field(36, ge=0)
    total_bc_limit: Optional[float] = Field(5400.0, ge=0)
    num_rev_tl_bal_gt_0: Optional[float] = Field(5.0, ge=0)
    purpose: str = "credit_card"
    loan_amnt: Optional[float] = Field(12000.0, ge=0)
    num_actv_bc_tl: Optional[float] = Field(3.0, ge=0)
    mo_sin_rcnt_tl: Optional[float] = Field(2.0, ge=0)
    mo_sin_rcnt_rev_tl_op: Optional[float] = Field(12.0, ge=0)
    acc_open_past_24mths: Optional[float] = Field(7.0, ge=0)
    home_ownership: str = "MORTGAGE"
    DTI_Category: str = "DTI < 15%"

    @property
    def fico_avg(self):
        if self.fico_range_low and self.fico_range_high:
            return (self.fico_range_high + self.fico_range_low) / 2
        return None

    @property
    def sec_app_fico_avg(self):
        if (
            self.sec_app_fico_range_high is not None
            and self.sec_app_fico_range_low is not None
        ):
            return (self.sec_app_fico_range_high + self.sec_app_fico_range_low) / 2
        return None

    @property
    def fico_diff(self):
        if self.fico_range_high is not None and self.fico_range_low is not None:
            return self.fico_range_high - self.fico_range_low
        return None

    @property
    def sec_app_fico_diff(self):
        if (
            self.sec_app_fico_range_high is not None
            and self.sec_app_fico_range_low is not None
        ):
            return self.sec_app_fico_range_high - self.sec_app_fico_range_low
        return None

    @property
    def loan_size_category(self):
        bins = [0, 5000, 10000, 20000, 30000, 40000, float("inf")]
        labels = ["< 5K", "5K - 10K", "10K - 20K", "20K - 30K", "30K - 40K", ">= 40K"]
        if self.loan_amnt is not None:
            return pd.cut([self.loan_amnt], bins=bins, labels=labels)[0]
        return None

    @property
    def DTI_Category(self):
        bins = [0, 15, 25, float("inf")]
        labels = ["DTI < 15%", "15% <= DTI <= 25%", "DTI > 25%"]
        if self.dti is not None:
            return pd.cut([self.dti], bins=bins, labels=labels)[0]
        return None

    @validator("grade")
    def grade_must_have_value(cls, value):
        if value not in GRADES_MAPPING.values():
            raise ValueError(
                f"expected grade values are {GRADES_MAPPING.values()}. Received value - {value}"
            )
        return value

    @validator("dti_joint")
    def dti_joint_validator(cls, value):
        if "float" in str(type(value)) or "int" in str(type(value)):
            if value < 0:
                raise ValueError("expected dti_joint values must be greater than 0.")
        elif value != "nan":
            raise ValueError("expected dti_joint value is 'nan' or numeric value.")
        return value

    @validator("home_ownership")
    def home_ownership_must_have_value(value):
        expected = ["MORTGAGE", "RENT", "OWN", "NONE", "ANY", "OTHER"]
        if value not in expected:
            raise ValueError(
                f"expected home_ownership values are {expected}. Received value - {value}"
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
            if col == "term":
                if val not in TERM_MAPPING.values():
                    data["term"] = [TERM_MAPPING[self.term]]
                else:
                    data["term"] = [self.term]
            else:
                data[col] = [val]

        if "sec_app_fico_avg" not in list(data.keys()):
            data["sec_app_fico_avg"] = [self.sec_app_fico_avg]

        if "fico_avg" not in list(data.keys()):
            data["fico_avg"] = [self.fico_avg]

        if "fico_diff" not in list(data.keys()):
            data["fico_diff"] = [self.fico_diff]

        if "DTI_Category" not in list(data.keys()):
            data["DTI_Category"] = [self.DTI_Category]

        if "loan_size_category" not in list(data.keys()):
            data["loan_size_category"] = [self.loan_size_category]

        if "sec_app_fico_diff" not in list(data.keys()):
            data["sec_app_fico_diff"] = [self.sec_app_fico_diff]

        return data


class LoanStep4(BaseModel):
    loan_amnt: Optional[float] = Field(25600.0, ge=0)
    term: Optional[int] = Field(60, ge=0)
    grade: str = "B"
    sub_grade: str = "B5"
    home_ownership: str = "MORTGAGE"
    annual_inc: Optional[float] = Field(70000.0, ge=0)
    verification_status: str = "Not Verified"
    purpose: str = "medical"
    dti: Optional[float] = Field(29.04, ge=0)
    fico_range_low: Optional[float] = Field(725.0, ge=0)
    fico_range_high: Optional[float] = Field(729.0, ge=0)
    open_acc: Optional[float] = Field(15.0, ge=0)
    revol_bal: Optional[float] = Field(26059.0, ge=0)
    application_type: str = "Joint App"
    annual_inc_joint: float = 96000.0
    dti_joint: float = 24.76
    verification_status_joint: str = "Not Verified"
    open_rv_12m: Optional[float] = Field(1.0, ge=0)
    open_rv_24m: Optional[float] = Field(1.0, ge=0)
    all_util: Optional[float] = Field(45.0, ge=0)
    total_rev_hi_lim: Optional[float] = Field(64900.0, ge=0)
    inq_fi: Optional[float] = Field(1.0, ge=0)
    inq_last_12m: Optional[float] = Field(3.0, ge=0)
    acc_open_past_24mths: Optional[float] = Field(4.0, ge=0)
    bc_open_to_buy: Optional[float] = Field(21583.0, ge=0)
    bc_util: Optional[float] = Field(51.6, ge=0)
    mo_sin_old_rev_tl_op: Optional[float] = Field(313.0, ge=0)
    mo_sin_rcnt_rev_tl_op: Optional[float] = Field(9.0, ge=0)
    mo_sin_rcnt_tl: Optional[float] = Field(3.0, ge=0)
    mort_acc: Optional[float] = Field(5.0, ge=0)
    num_rev_accts: Optional[float] = Field(17.0, ge=0)
    num_tl_op_past_12m: Optional[float] = Field(2.0, ge=0)
    percent_bc_gt_75: Optional[float] = Field(20.0, ge=0)
    total_bc_limit: Optional[float] = Field(44600.0, ge=0)
    revol_bal_joint: float = 40627.0
    sec_app_fico_range_low: float = 705.0
    sec_app_fico_range_high: float = 709.0
    sec_app_mort_acc: float = 5.0
    sec_app_open_acc: float = 11.0
    sec_app_num_rev_accts: float = 13.0

    @property
    def fico_avg(self):
        if self.fico_range_high is not None and self.fico_range_low is not None:
            return (self.fico_range_high + self.fico_range_low) / 2
        return None

    @property
    def sec_app_fico_avg(self):
        if (
            self.sec_app_fico_range_high is not None
            and self.sec_app_fico_range_low is not None
        ):
            return (self.sec_app_fico_range_high + self.sec_app_fico_range_low) / 2
        return None

    @property
    def fico_diff(self):
        if self.fico_range_high is not None and self.fico_range_low is not None:
            return self.fico_range_high - self.fico_range_low
        return None

    @property
    def sec_app_fico_diff(self):
        if (
            self.sec_app_fico_range_high is not None
            and self.sec_app_fico_range_low is not None
        ):
            return self.sec_app_fico_range_high - self.sec_app_fico_range_low
        return None

    @property
    def LTI(self):
        if self.annual_inc_joint is not None:
            return self.loan_amnt / self.annual_inc_joint
        elif self.annual_inc_joint is not None:
            return self.loan_amnt / self.annual_inc
        return None

    @property
    def DTI_Category(self):
        bins = [0, 15, 25, float("inf")]
        labels = ["DTI < 15%", "15% <= DTI <= 25%", "DTI > 25%"]
        if self.dti is not None:
            return pd.cut([self.dti], bins=bins, labels=labels)[0]
        return None

    @property
    def loan_size_category(self):
        bins = [0, 5000, 10000, 20000, 30000, 40000, float("inf")]
        labels = ["< 5K", "5K - 10K", "10K - 20K", "20K - 30K", "30K - 40K", ">= 40K"]
        if self.loan_amnt is not None:
            return pd.cut([self.loan_amnt], bins=bins, labels=labels)[0]
        return None

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
    def dti_joint_validator(cls, value):
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

        if "sec_app_fico_avg" not in list(data.keys()):
            data["sec_app_fico_avg"] = [self.sec_app_fico_avg]

        if "fico_avg" not in list(data.keys()):
            data["fico_avg"] = [self.fico_avg]

        if "LTI" not in list(data.keys()):
            data["LTI"] = [self.LTI]

        if "fico_diff" not in list(data.keys()):
            data["fico_diff"] = [self.fico_diff]

        if "DTI_Category" not in list(data.keys()):
            data["DTI_Category"] = [self.DTI_Category]

        if "loan_size_category" not in list(data.keys()):
            data["loan_size_category"] = [self.loan_size_category]

        if "sec_app_fico_diff" not in list(data.keys()):
            data["sec_app_fico_diff"] = [self.sec_app_fico_diff]

        return data
