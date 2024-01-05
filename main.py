import glob

from bs4 import BeautifulSoup
import pandas as pd


def parse():
    files = glob.glob("/home/mvl/work/hh_parser/download_pages/*.html")

    df = pd.DataFrame(
        columns=["industry", "region", "city", "vacancy_dynamics", "resume_dynamics", "hh_index", "salary"],
    )

    for file in files:
        with open(f"{file}") as f:
            src = f.read()

            soup = BeautifulSoup(src, "lxml")

            industry = soup.find("div", class_="_comparisonTableTitle_1rq97_121").text.strip()

            rows = soup.find_all(class_="_comparisonTableRow_1rq97_118 _comparisonTableContent_1rq97_171")

            for row in rows:
                columns = row.find_all("div")

                new_row = pd.DataFrame({
                    "industry": industry,
                    "region": columns[0].text.strip(),
                    "city": columns[1].text.strip(),
                    "vacancy_dynamics": columns[2].text.strip(),
                    "resume_dynamics": columns[3].text.strip(),
                    "hh_index": columns[4].text.split("/")[0].strip().replace(".", ","),
                    "salary": columns[5].text.split("/")[0].strip(),
                }, index=[0])

                df = pd.concat([df, new_row], ignore_index=True)

    df.to_excel("output.xlsx", index=False)


if __name__ == "__main__":
    parse()
