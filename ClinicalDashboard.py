import streamlit as st
import pandas as pd
from scipy import stats

st.title("Clinical Trial Data Analyzer")

st.write("Upload clinical trial data to clean, standardize, and analyze treatment effectiveness.")

st.write("### How to Use")
st.write("""
1. Upload your dataset  
2. Map the required columns  
3. View analysis results  
""")

st.divider()

uploaded_file = st.file_uploader(
    "Upload your clinical trial dataset (CSV)",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

    st.write("### Dataset Overview")
    st.write(f"Rows: {df.shape[0]}")
    st.write(f"Columns: {df.shape[1]}")

    if df.shape[0] == 0:
        st.error("Dataset is empty. Please upload a valid file.")
        st.stop()

    if df.shape[1] < 3:
        st.error("Dataset must contain at least 3 columns.")
        st.stop()

    st.write("### Columns in Dataset")
    st.write(list(df.columns))

    st.write("### Data Preview")
    st.dataframe(df.head())

    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    #common clinical trial BP naming conventions:

    baseline_aliases = [
        
        # generic baseline names:

        "baseline_bp",
        "baselinebloodpressure",
        "baseline_blood_pressure",
        "bp_baseline",
        "base_bp",
        "basebp",
        "baseline",

        #systolic specific names:

        "sbp_baseline",
        "baseline_sbp",
        "base_sbp",
        "sbp_base",
        "sysbp_base",
        "sys_bp_base",
        "baseline_sysbp",
        "baseline_sys_bp",
        "systolic_baseline",
        "baseline_systolic",
        "baseline_systolic_bp",

        # visit-based:

        "visit1_bp",
        "visit1_sbp",
        "screening_bp",
        "screening_sbp",
        "pre_treatment_bp",
        "pretreatment_bp",
        "day0_bp",
        "day_0_bp",
        "week0_bp",
        "week_0_bp",

        # CDISC-ish styles:

        "aval_base",
        "base",
        "baseval",
        "chgbase_bp",
        "paramcd_sysbp_base",

        # weird real-world naming:

        "initial_bp",
        "initial_sbp",
        "starting_bp",
        "starting_sbp",
        "enrollment_bp",
        "entry_bp",
        "admission_bp"

    ]

    followup_aliases = [

        # generic follow-up names
        "followup_bp",
        "follow_up_bp",
        "followupbloodpressure",
        "followup_blood_pressure",
        "bp_followup",
        "final_bp",
        "post_bp",
        "ending_bp",

        # systolic-specific
        "sbp_followup",
        "followup_sbp",
        "final_sbp",
        "endpoint_sbp",
        "sysbp_followup",
        "sys_bp_followup",
        "post_treatment_sbp",
        "systolic_followup",
        "followup_systolic",
        "followup_systolic_bp",

        # visit/timepoint-based
        "visit2_bp",
        "visit3_bp",
        "visit4_bp",
        "week4_bp",
        "week8_bp",
        "week12_bp",
        "week16_bp",
        "week24_bp",
        "week52_bp",

        "week4_sbp",
        "week8_sbp",
        "week12_sbp",
        "week16_sbp",
        "week24_sbp",

        "day30_bp",
        "day60_bp",
        "day90_bp",

        # endpoint/final
        "endpoint_bp",
        "study_end_bp",
        "exit_bp",
        "termination_bp",
        "discharge_bp",

        # CDISC-ish
        "aval",
        "chg",
        "postbase_bp",
        "analysis_bp",

        # miscellaneous
        "latest_bp",
        "current_bp",
        "observed_bp",
        "measurement_bp"
    ]

    patient_id_aliases = [
        # generic
        "patient_id", 
        "patientid", 
        "patient_id_number", 
        "pid",
        "pt_id", 
        "ptid", 
        "pt_num", 
        "patient_number",
        
        # subject-based
        "subject_id", 
        "subjectid", 
        "subject_number", 
        "sub_id",
        "subid", 
        "subject", 
        "subjid", 
        "subj_id",
        
        # CDISC/SDTM style
        "usubjid", 
        "subjid", 
        "siteid", 
        "randid",
        
        # study-based
        "study_id", 
        "studyid", 
        "study_patient_id",
        "enrollment_id", 
        "enroll_id", 
        "trial_id",
        
        # participant-based
        "participant_id", 
        "participantid", 
        "part_id",
        "partid", 
        "participant_number", 
        "participant",
        
        # case/record-based
        "case_id", 
        "caseid", 
        "record_id", 
        "recordid",
        "case_number", 
        "record_number",
        
        # hospital/clinical
        "mrn", 
        "medical_record_number", 
        "hospital_id",
        "chart_id", 
        "patient_code", 
        "pt_code",
        
        # numbered
        "id", 
        "ID", 
        "Id", 
        "no", 
        "number", 
        "num",
        "patient_no", 
        "pt_no", 
        "subject_no"

        ]

    age_aliases = [

        # generic
        "age", 
        "age_years", 
        "age_yr", 
        "age_yrs",
        "patient_age", 
        "pt_age", 
        "subject_age",

        # baseline/enrollment
        "age_baseline", 
        "age_at_baseline", 
        "age_enrollment",
        "age_at_enrollment", 
        "age_at_entry", 
        "age_entry",
        "age_at_screening", 
        "screening_age", 
        "age_screen",

        # CDISC-ish
        "agebsl", 
        "ageb", 
        "age_bsl", 
        "age0",
        "agecat", 
        "agegr", 
        "agegr1",

        # visit-based
        "age_visit1", 
        "age_v1", 
        "age_day0",
        "age_week0", 
        "age_at_visit",

        # demographic
        "demo_age", 
        "demographic_age", 
        "dob_derived",
        "calculated_age", 
        "computed_age",

        # real-world variations
        "current_age", 
        "reported_age", 
        "age_reported",
        "age_confirmed", 
        "age_verified",
        "years_old", 
        "yrs_old", 
        "yr_old"
    ]

    sex_aliases = [

        # generic
        "sex", 
        "gender", 
        "sex_gender",
        "patient_sex", 
        "patient_gender",
        "subject_sex", 
        "subject_gender",
        "pt_sex", 
        "pt_gender",

        # biological
        "biological_sex", 
        "sex_at_birth",
        "birth_sex", 
        "assigned_sex",
        "sex_assigned_at_birth",

        # CDISC/SDTM
        "sex_cd", 
        "sexcd", 
        "gndr",
        "gender_cd", 
        "gendercd",

        # demographic
        "demo_sex", 
        "demo_gender",
        "demographic_sex", 
        "demographic_gender",

        # coded
        "sex_code", 
        "gender_code",
        "sex_label", 
        "gender_label",
        "sex_value", 
        "gender_value",

        # real-world variations
        "reported_sex", 
        "reported_gender",
        "sex_reported", 
        "gender_reported",
        "self_reported_sex", 
        "self_reported_gender",
        "sex_confirmed", 
        "gender_confirmed"
    ]

    treatment_aliases = [

        # generic
        "treatment", 
        "treatment_group", 
        "treatment_arm",
        "trt", "trt_group", 
        "trt_arm",

        # arm-based
        "arm", 
        "study_arm", 
        "trial_arm",
        "randomization_arm", 
        "rand_arm",
        "assigned_arm", 
        "arm_label",

        # drug-based
        "drug", 
        "drug_name", 
        "drug_group",
        "medication", 
        "med", 
        "med_group",
        "compound", 
        "compound_name",

        # intervention
        "intervention", 
        "intervention_group",
        "intervention_arm", 
        "intervention_label",

        # CDISC/SDTM
        "actarm", 
        "actarmcd", 
        "arm_cd",
        "armcd", 
        "trtcd", 
        "trt_cd",
        "planned_arm", 
        "actual_arm",

        # randomization
        "rand_group", 
        "randomized_group",
        "randomization_group", 
        "rand_trt",
        "randomized_treatment",

        # cohort/group
        "cohort", 
        "cohort_group", 
        "group",
        "study_group", 
        "trial_group",
        "dose_group", 
        "dose_arm",

        # real-world variations
        "assigned_treatment", 
        "treatment_assigned",
        "treatment_label", 
        "treatment_code",
        "treatment_name", 
        "therapy",
        "therapy_group", 
        "therapy_arm"
    ]
        

    baseline_col = None

    for col in baseline_aliases:
        if col in df.columns:
            baseline_col = col
            break

    followup_col = None

    for col in followup_aliases:
        if col in df.columns:
            followup_col = col
            break

    pid_col = None

    for col in patient_id_aliases:
        if col in df.columns:
            pid_col = col
            break
    
    age_col = None

    for col in age_aliases:
        if col in df.columns:
            age_col = col
            break

    sex_col = None

    for col in sex_aliases:
        if col in df.columns:
            sex_col = col
            break

    treatment_col = None

    for col in treatment_aliases:
        if col in df.columns:
            treatment_col = col
            break

    cols = set(df.columns)

    if {"baseline_bp", "followup_bp"}.issubset(cols):
        data_format = "ADAM"

    elif {"visit", "test", "value"}.issubset(cols):
        data_format = "SDTM"
    
    else:
        data_format = "UNKNOWN"
        
    
    pid_col = st.selectbox(
        "Select Patient ID Column",
        options = df.columns,
        index = (df.columns.get_loc(pid_col)) if pid_col in df.columns else 0
    )

    age_col = st.selectbox(
        "Select Age Column",
        options = df.columns,
        index = (df.columns.get_loc(age_col)) if age_col in df.columns else 0
    )

    sex_col = st.selectbox(
        "Select sex/gender column",
        options = df.columns,
        index = (df.columns.get_loc(sex_col)) if sex_col in df.columns else 0
    )

    treatment_col = st.selectbox(
        "Select Treatment column",
        options = df.columns,
        index = (df.columns.get_loc(treatment_col)) if treatment_col in df.columns else 0

    )

    baseline_col = st.selectbox(
        "Select Baseline Blood Pressure Column",
        options = df.columns,
        index = (df.columns.get_loc(baseline_col)) if baseline_col in df.columns else 0

    )

    followup_col = st.selectbox(
        "Select Follow-up Blood Pressure Column",
        options = df.columns,
        index = (df.columns.get_loc(followup_col)) if followup_col in df.columns else 0
    
    )



    col_list = [pid_col, age_col, sex_col, treatment_col, baseline_col, followup_col]

    if len(col_list) != len(set(col_list)):
        st.error("Please select unique columns for each field.")
        st.stop()
    
    if any(col is None for col in col_list):
         st.error("please select a column for each field")
         st.stop()

    def validate_age(series):
        return(
            pd.api.types.is_numeric_dtype(series) and
            series.dropna().between(0,120).mean() > 0.9
        )

    def validate_sex(series):
        allowed = {"male" , "female" , "m" , "f"}
        values  = set(series.dropna().astype(str).str.lower())
        return len(values.intersection(allowed)) > 0

    def validate_treatment(series):
        return series.nunique() <= 10

    def validate_bp(series):
        numeric = pd.to_numeric(series, errors = "coerce")
        return numeric.dropna().between(50,250).mean() > 0.9
        

    def validate_patient_id(series):
        return series.nunique() == len(series) and series.isnull().sum() == 0
    
    validators = {
        "patient_id": validate_patient_id,
        "age": validate_age,
        "sex": validate_sex,
        "treatment": validate_treatment,
        "baseline_bp": validate_bp,
        "followup_bp": validate_bp
    }

    mapping = {
        "patient_id": pid_col,
        "age": age_col,
        "sex": sex_col,
        "treatment": treatment_col,
        "baseline_bp": baseline_col,
        "followup_bp": followup_col
    }

    errors = []

    for field, col in mapping.items():
        
        if col not in df.columns:
            errors.append(f"{field}: column '{col}' not found in dataset")
            continue
        
        series = df[col]

        if field not in validators:
            errors.append(f"{field}: no validator defined")
            continue

        is_valid = validators[field](series)

        if not is_valid:

            if field == "age":
                msg = f"Age column '{col}' failed validation (expected numeric values mostly between 0–120)"
        
            elif field == "sex":
                msg = f"Sex column '{col}' failed validation (expected values like M/F or male/female)"
            
            elif field == "treatment":
                msg = f"Treatment column '{col}' failed validation (expected low-cardinality categorical values)"
            
            elif field in ["baseline_bp", "followup_bp"]:
                msg = f"BP column '{col}' failed validation (expected numeric values in realistic range)"
            
            else:
                msg = f"{field} column '{col}' failed validation"

            errors.append(msg)

    if errors:
        for e in errors:
            st.error(e)
        st.stop()
    else:
        st.success("Data validation passed")

        clean_df = df.copy()

        #standardization of sex column

        clean_df[sex_col] = (
            clean_df[sex_col]
            .astype(str)
            .str.lower()
            .replace({
                "m": "male",
                "f": "female"
            })
        )

        #converting age to numeric 

        clean_df[age_col] = pd.to_numeric(
            clean_df[age_col],
            errors = "coerce"
        )

        #removing possible outliers in age

        clean_df.loc[
            (clean_df[age_col] < 18)|
            (clean_df[age_col] > 120),
            age_col
        ] = pd.NA


        #converting baseline bp to numeric

        clean_df[baseline_col] = pd.to_numeric(
            clean_df[baseline_col],
            errors = "coerce"
        )

        #converting follow-up bp to numeric

        clean_df[followup_col] = pd.to_numeric(
            clean_df[followup_col],
            errors = "coerce"
        )

        #feature engineering header

        st.header("Feature engineering")

        #blood pressure changes

        clean_df["bp_change"] = (
            clean_df[baseline_col] - clean_df[followup_col]

        )


        clean_df["risk_group"] = clean_df[age_col].apply(
            lambda x:
                "unknown" if pd.isnull(x)
                else "high" if x >= 60
                else "low"
        )

        #improvement flag

        clean_df["response_category"] = clean_df["bp_change"].apply(
            lambda x:
                "unknown" if pd.isnull(x)
                else "improved" if x > 0
                else "no change" if x == 0
                else "worsened"
        )

        st.success("Analysis complete!")
        st.header("Cleaned Dataset")
        st.dataframe(clean_df.head())
        st.header("Blood pressure change distribution")  

        bp_bins = pd.cut(
            clean_df["bp_change"].dropna(),
            bins = 10,
        )      

        bp_counts = bp_bins.value_counts().sort_index()
        bp_counts.index = bp_counts.index.astype(str)

        st.bar_chart(bp_counts)

        # grouping by treatment and risk group, then visualizing

        treatment_summary = (
            clean_df
            .groupby([treatment_col, "risk_group"])["bp_change"]
            .agg(["count", "mean", "median", "std"])
            .round(2)
        )

        treatment_summary.columns = ["Patient Count", "Mean BP Change" , "Median BP Change", "Std Dev"]

        st.dataframe(treatment_summary)

        st.subheader("Average BP change by treatment")

        avg_bp_change = (
            clean_df
            .groupby([treatment_col, "risk_group"])["bp_change"]
            .mean()
            .round(2)
            .reset_index()
        )

        avg_bp_change.columns = ["Treatment", "Risk Group" , "Mean BP Change"]

        st.dataframe(avg_bp_change)


        st.bar_chart(avg_bp_change.set_index("Treatment")["Mean BP Change"])

        #response category breakdown

        st.subheader("Response Category by Treatment")

        response_summary = (
            clean_df
            .groupby([treatment_col, "response_category"])["bp_change"]
            .count()
            .reset_index()
        )

        response_summary.columns = ["Treatment" , "Response Category" , "Patient Count"]

        st.dataframe(response_summary)

        # missing data report

        st.header("Missing Data Report")

        missing = clean_df.isnull().sum()
        missing_pct = (clean_df.isnull().sum() / len(clean_df) *100).round(2)

        missing_report = pd.DataFrame({
            "Missing Values": missing,
            "Percentage missing": missing_pct
        })

        missing_report = missing_report[missing_report["Missing Values"] > 0]

        st.dataframe(missing_report) 

        st.header("Download Cleaned Dataset")

        csv = clean_df.to_csv(index = False)

        st.download_button(
            label = "Download cleaned dataset as CSV",
            data = csv,
            file_name = "cleaned_trial_data.csv",
            mime = "text/csv"
        )

        st.header("Statistical Testing")
        
        control_group = st.selectbox(
            "Select Control/Placebo Group",
            options = clean_df[treatment_col].unique()

        )

        placebo_bp = clean_df[clean_df[treatment_col] == control_group]["bp_change"].dropna()

        treatment_groups = clean_df[treatment_col].unique()

        for group in treatment_groups:
            if group == control_group:
                continue

            group_bp = clean_df[clean_df[treatment_col] == group]["bp_change"].dropna()

            t_stat, p_value = stats.ttest_ind(group_bp, placebo_bp)

            st.subheader(f"{group} vs {control_group}")
            st.write(f"P-value: {round(p_value, 4)}")

            group_mean = group_bp.mean()
            control_mean = placebo_bp.mean()
            
            if p_value < 0.05:
                if group_mean > control_mean:
                    st.success(f"Statistcally significant improvement in blood pressure for {group} compared to {control_group}")
                else:
                    st.error(f"Statistically significant — but {group} performed WORSE than control")
            else:
                st.warning(f"Not statistically significant, no strong evidence {group} had any real effect on patients")
        
        st.header("Demographic Summary")

        #patient count by treatment and sex

        st.subheader("Patient count by treatment and sex")

        sex_counts = (
            clean_df
            .groupby([treatment_col, sex_col])[pid_col]
            .count()
            .reset_index()
        )

        sex_counts.columns = ["Treatment" , "Sex", "Patient Count"]

        st.dataframe(sex_counts)
            
        # age distribution by treatment
        
        st.subheader("Age Distribution by treatment")

        age_summary = (
            clean_df.groupby(treatment_col)[age_col]
            .agg(["mean", "median", "std", "min", "max"])                
            .round(2)
        
        )

        age_summary.columns = ["Mean Age", "Median Age", "Std Dev", "Min Age", "Max Age"]

        st.dataframe(age_summary)

        #risk group counts by treatment

        st.subheader("Risk Group Distribution by Treatment")

        risk_counts = (
            clean_df
            .groupby([treatment_col, "risk_group"])[pid_col]
            .count()
            .reset_index()

        )

        risk_counts.columns = ["Treatment" , "Risk Group" , "Patient Count"]

        st.dataframe(risk_counts)
        


