import pandas as pd

def preprocess_dataset(file_path):
    import pandas as pd

    df = pd.read_csv(file_path)
    df.fillna("Unknown", inplace=True)

    docs = []

    # Row-level records (existing)
    for idx, row in df.iterrows():
        text = "\n".join([f"{col}: {row[col]}" for col in df.columns])
        docs.append(text)

    # Aggregated Insights
    approval_by_credit = df.groupby("Credit_History")["Loan_Status"].value_counts().unstack().fillna(0)
    docs.append("Loan approval stats by credit history:\n" + str(approval_by_credit))

    approval_by_education = df.groupby("Education")["Loan_Status"].value_counts().unstack().fillna(0)
    docs.append("Loan approval stats by education:\n" + str(approval_by_education))

    approval_by_gender = df.groupby("Gender")["Loan_Status"].value_counts().unstack().fillna(0)
    docs.append("Loan approval stats by gender:\n" + str(approval_by_gender))

    approval_by_area = df.groupby("Property_Area")["Loan_Status"].value_counts().unstack().fillna(0)
    docs.append("Loan approval stats by property area:\n" + str(approval_by_area))

    return docs
