'''import pandas as pd
import numpy as np

df = pd.DataFrame({
    "patient_id": [201,202,203,204,205,206,207,208],
    "age": [23, 67, None, 45, 150, 34, 29, None],
    "sex": ["M", "female", "F", "Male", "f", None, "Female", "M"],
    "treatment": ["A","B","A","Placebo","B","A","Placebo","B"],
    "baseline_bp": [150, 160, 145, None, 170, 155, 148, 165],
    "followup_bp": [140, "error", 130, 135, 160, None, 142, 150],
    "lab_result": [7.2, 15.5, "missing", -3, 8.1, 9.0, 50, None]
})

df.info()
df.describe(include = "all")

df["sex"] =df["sex"].str.lower()
df["sex"] =  df["sex"].replace({"m": "male", "f": "female"})
df.loc[(df["sex"].isnull()), "sex"] = "unknown"

df.loc[(df["age"] < 18) | (df["age"] > 120), "age"] = np.nan
df["followup_bp"] = pd.to_numeric(df["followup_bp"] , errors = "coerce")
df["lab_result"] = pd.to_numeric(df["lab_result"] , errors = "coerce")


df.loc[(df["lab_result"] < 0) | (df["lab_result"] > 20), "lab_result"] = np.nan

df["baseline_bp"] = pd.to_numeric(df["baseline_bp"] , errors = "coerce")
df["bp_change"] = df["baseline_bp"] - df["followup_bp"]


df["risk_group"] = df["age"].apply(
    lambda x: "unknown" if pd.isnull(x)
    else "high" if x >= 60
    else "low"
)

df.info()
df.describe(include = "all")'''

import pandas as pd
import numpy as np

np.random.seed(1)

df = pd.DataFrame({
    "patient_id": range(1001, 1021),
    "age": [25, 67, None, 45, 150, 34, 29, None, 52, 61, 70, None, 80, 22, 40, 38, None, 55, 63, 77],
    "sex": ["M", "female", "F", "Male", "f", None, "Female", "M", "male", "F",
            "Male", "female", None, "F", "M", "Female", "male", None, "F", "Male"],
    "treatment": ["A","B","A","Placebo","B","A","Placebo","B","A","Placebo",
                  "B","A","Placebo","A","B","Placebo","A","B","Placebo","A"],
    "baseline_bp": [150, 160, 145, None, 170, 155, 148, 165, 158, None,
                    172, 149, 151, 140, 168, 152, 147, 166, 159, 161],
    "followup_bp": [140, "error", 130, 135, 160, None, 142, 150, "error", 138,
                    155, 140, None, 130, 158, 148, 135, None, 150, 149],
    "lab_result": [7.2, 15.5, "missing", -3, 8.1, 9.0, 50, None, 6.8, 7.5,
                   12.1, 5.5, 8.0, 6.2, 9.8, None, 7.1, 20.5, 8.3, 7.9]
})



df.loc[(df["age"].isNull()) , "age"] = df["age"].mean()
df["sex"] = df["sex"].str.toLower()
df["sex"] = df["sex"].replace({"m": male, "f": "female"})

df["followup_bp"] = pd.to_numeric(df["followup_bp"], errors = "coerce")
df["lab_result"] = pd.to_numeric(df["lab_result"], errors = "coerce")


df.loc[(df["age"] < 18) | (df["age"] > 120) , "age"] = np.nan

df["bp_change"] = df["baseline_bp"] - df["followup_bp"]

df["risk_group"] = df["age"].apply(
    lambda x: 
    "unknown" if pd.isNull(x)
    else "high" if x >= 60
    else "low"
)

df["lab_high"] = df["lab_result"].apply(
    lambda x:
    "high" if x > 10
)

df.groupby("treatment")["bp_change"].mean()

df.groupby("treatment")["patient_id"].nunique()

df.groupby(["treatment", "risk_group"])["bp_change"].mean()






