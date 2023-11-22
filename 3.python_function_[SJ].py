import pandas as pd


class Loan:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def read_csv(self):
        """This function is used to read CSV using pandas and rename the columns."""
        data = pd.read_csv(self.csv_file)
        data.rename(
            columns={
                "col 1": "loan_id",
                "col 2": "fc_flag",
                "col 3": "bk_flag",
                "col 4": "month_dq",
            },
            inplace=True,
        )
        return data

    @classmethod
    def status(self, each_row):
        """Define the ‘dq_status’ of the loan based on the bk_flag, fc_flag, and month_dq."""
        if each_row["bk_flag"] == 1:
            return "BK"
        elif each_row["fc_flag"] == 1:
            return "FC"
        else:
            month_dq = each_row["month_dq"]
            if month_dq >= 6:
                return "D180+"
            if month_dq == 5:
                return "D150"
            if month_dq == 4:
                return "D120"
            if month_dq == 3:
                return "D90"
            if month_dq == 2:
                return "D60"
            if month_dq == 1:
                return "D30"
            if month_dq == 0:
                return "Current"

    def loan(self):
        """Calculate how many loans each ‘dq_status’ (BK, FC, D180+, D150, D120, D90, D60, D30, Current) has."""
        # Read CSV using pandas and rename the columns
        data = self.read_csv()
        # Call the status method using a lambda function and set the 'dq_status' column
        data["dq_status"] = data.apply(lambda row: self.status(row), axis=1)
        # Count the number of loans by 'dq_status' and write the output to a new file
        new_data = data.groupby("dq_status")["dq_status"].agg(count="count")
        new_data.to_csv("output.csv")


if __name__ == "__main__":
    analyzer = Loan("3. Python Question.csv")
    analyzer.loan()
