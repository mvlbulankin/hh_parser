import glob

from bs4 import BeautifulSoup
import pandas as pd


def parse():
    files = glob.glob(r"C:\work\hh_parser\download_pages_fix\*.html")

    df = pd.DataFrame(
        columns=[
            "last_day_mnth",
            "industry",
            "region",
            "city",
            "vacancy_dynamics",
            "resume_dynamics",
            "hh_index",
            "median_salary"
        ],
    )

    for file in files:
        with open(f"{file}", encoding="utf-8") as f:
            src = f.read()

        soup = BeautifulSoup(src, "lxml")
        last_day_mnth = "2023-03-31"
        industry = soup.find("div", class_="_comparisonTableTitle_1rq97_121").text.strip()
        rows = soup.find_all(class_="_comparisonTableRow_1rq97_118 _comparisonTableContent_1rq97_171")

        for row in rows:
            columns = row.find_all("div")

            region = columns[0].text.strip()
            city = columns[1].text.strip()

            vacancy_dynamics = columns[2].text.strip().replace("%", "")
            if vacancy_dynamics != "-":
                vacancy_dynamics = int(vacancy_dynamics)
            else:
                vacancy_dynamics = None

            resume_dynamics = columns[3].text.strip().replace("%", "")
            if resume_dynamics != "-":
                resume_dynamics = int(resume_dynamics)
            else:
                resume_dynamics = None

            hh_index = columns[4].text.split("/")[0].strip()
            if hh_index != "-":
                hh_index = float(hh_index)
            else:
                hh_index = None

            median_salary = columns[5].text.split("/")[0].strip().replace(",", ".")
            if median_salary != "-":
                median_salary = float(median_salary)
            else:
                median_salary = None

            new_row = pd.DataFrame({
                "last_day_mnth": last_day_mnth,
                "industry": industry,
                "region": region,
                "city": city,
                "vacancy_dynamics": vacancy_dynamics,
                "resume_dynamics": resume_dynamics,
                "hh_index": hh_index,
                "median_salary": median_salary,
            }, index=[0])

            df = pd.concat([df, new_row], ignore_index=True)

    df.to_excel("hh_data_2023_03_finance.xlsx", index=False)
    df.to_csv("hh_data_2023_03_finance.csv", index=False)

    print("All data loaded")


if __name__ == "__main__":
    parse()
