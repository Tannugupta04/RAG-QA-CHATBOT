# import pandas as pd

# def preprocess_dataset(file_path):
#     import pandas as pd

#     df = pd.read_csv(file_path)
#     df.fillna("Unknown", inplace=True)

#     docs = []

#     # Row-level records (existing)
#     for idx, row in df.iterrows():
#         text = "\n".join([f"{col}: {row[col]}" for col in df.columns])
#         docs.append(text)

#     # Aggregated Insights
#     approval_by_credit = df.groupby("Credit_History")["Loan_Status"].value_counts().unstack().fillna(0)
#     docs.append("Loan approval stats by credit history:\n" + str(approval_by_credit))

#     approval_by_education = df.groupby("Education")["Loan_Status"].value_counts().unstack().fillna(0)
#     docs.append("Loan approval stats by education:\n" + str(approval_by_education))

#     approval_by_gender = df.groupby("Gender")["Loan_Status"].value_counts().unstack().fillna(0)
#     docs.append("Loan approval stats by gender:\n" + str(approval_by_gender))

#     approval_by_area = df.groupby("Property_Area")["Loan_Status"].value_counts().unstack().fillna(0)
#     docs.append("Loan approval stats by property area:\n" + str(approval_by_area))

#     return docs

import pandas as pd


def preprocess_dataset(file_path):
    df = pd.read_csv(file_path)
    return preprocess_dataframe(df)


def preprocess_dataframe(df):
    df = df.copy()

    docs = []

    # Fill missing values safely
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    categorical_cols = df.select_dtypes(include=["object"]).columns

    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    df[categorical_cols] = df[categorical_cols].fillna("Unknown")

    # Row-level records
    for idx, row in df.iterrows():
        text = f"Record {idx + 1}:\n"
        text += "\n".join([f"{col}: {row[col]}" for col in df.columns])
        docs.append(text)

    # General dataset summary
    docs.append(f"Dataset summary: Total rows = {df.shape[0]}, Total columns = {df.shape[1]}")
    docs.append("Column names: " + ", ".join(df.columns))

    # Numeric summaries
    for col in numeric_cols:
        docs.append(f"""
Numeric summary for {col}:
Average: {df[col].mean():.2f}
Minimum: {df[col].min()}
Maximum: {df[col].max()}
Total: {df[col].sum():.2f}
""")

    # Categorical value counts
    for col in categorical_cols:
        value_counts = df[col].value_counts().to_string()
        docs.append(f"Value counts for {col}:\n{value_counts}")

    # Loan-specific insights
    if "Loan_Status" in df.columns:
        approved_count = (df["Loan_Status"] == "Y").sum()
        rejected_count = (df["Loan_Status"] == "N").sum()
        total_count = len(df)

        approval_rate = (approved_count / total_count) * 100 if total_count > 0 else 0

        docs.append(f"Total loan applications: {total_count}")
        docs.append(f"Total approved loans: {approved_count}")
        docs.append(f"Total rejected loans: {rejected_count}")
        docs.append(f"Loan approval rate: {approval_rate:.2f}%")

        group_columns = [
            "Credit_History",
            "Education",
            "Gender",
            "Property_Area",
            "Self_Employed",
            "Married",
            "Dependents"
        ]

        for col in group_columns:
            if col in df.columns:
                grouped = (
                    df.groupby(col)["Loan_Status"]
                    .value_counts()
                    .unstack()
                    .fillna(0)
                )
                docs.append(f"Loan approval stats by {col}:\n{grouped}")

        if "LoanAmount" in df.columns:
            df["LoanAmount"] = pd.to_numeric(df["LoanAmount"], errors="coerce")
            df["LoanAmount"] = df["LoanAmount"].fillna(df["LoanAmount"].median())

            approved_avg = df[df["Loan_Status"] == "Y"]["LoanAmount"].mean()
            rejected_avg = df[df["Loan_Status"] == "N"]["LoanAmount"].mean()

            docs.append(f"Average loan amount for approved applicants: {approved_avg:.2f}")
            docs.append(f"Average loan amount for rejected applicants: {rejected_avg:.2f}")

    return docs